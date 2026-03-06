from rest_framework import viewsets, status, permissions # Added standard permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Sum  # <--- CRITICAL: Add this for .aggregate(Sum(...))
from .models import Bid, JobPost, Order
from .serializers import BidSerializer, OrderSerializer

class MarketplaceStatsView(APIView):
    # Using standard IsAuthenticated to be safe
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        is_tailor = getattr(user, 'role', 'customer') == 'tailor'

        if is_tailor:
            # Aggregate returns a dictionary, 'or 0' handles cases with no orders
            total_sales = Order.objects.filter(item__user=user).aggregate(Sum('total_price'))['total_price__sum'] or 0
            active_bids = Bid.objects.filter(tailor=user, status='pending').count()
            total_orders = Order.objects.filter(item__user=user).count()
            
            return Response({
                "total_revenue": total_sales,
                "active_bids": active_bids,
                "orders_count": total_orders,
                "role": "tailor"
            })
        else:
            total_spent = Order.objects.filter(buyer=user).aggregate(Sum('total_price'))['total_price__sum'] or 0
            active_jobs = JobPost.objects.filter(customer__user=user, is_active=True).count()
            my_orders = Order.objects.filter(buyer=user).count()

            return Response({
                "total_spent": total_spent,
                "active_jobs": active_jobs,
                "orders_placed": my_orders,
                "role": "customer"
            })

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer

    def get_queryset(self):
        user = self.request.user
        # Checking role from the user's Profile
        if hasattr(user, 'profile') and user.profile.role == 'tailor':
            # Tailors act as "sellers" when selling fabric/items
            return Order.objects.filter(item__user=user)
        
        # Customers see the materials they have bought
        return Order.objects.filter(buyer=user)

    def perform_create(self, serializer):
        item = serializer.validated_data['item']
        qty = serializer.validated_data['quantity']
        
        # 1. Calculate price based on Seller's price (Inventory Logic)
        total = item.price_per_yard * qty
        
        # 2. Save the order with the calculated total
        order = serializer.save(buyer=self.request.user, total_price=total)
        
        # 3. Inventory Management: Decrease stock
        # Using decimal/float check for yards
        item.yards -= qty
        if item.yards <= 0:
            item.yards = 0
            item.is_available = False
        item.save()

        # 4. Optional: Trigger a notification to the seller
        # notify_seller_of_new_order(order)
        
class BidViewSet(viewsets.ModelViewSet):
    queryset = Bid.objects.all()
    serializer_class = BidSerializer

    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        bid = self.get_object()
        job = bid.job

        # 1. Validation: Only the customer who posted the job can accept a bid
        # Note: Accessing the customer's user through the profile relationship
        if job.customer.user != request.user:
            return Response({"error": "Unauthorized. You did not post this job."}, 
                            status=status.HTTP_403_FORBIDDEN)

        # 2. Update Bid and Job Status
        bid.status = 'accepted'
        bid.save()
        job.is_active = False
        job.save()

        # 3. Create the Project (The service contract)
        from projects.models import Project
        project = Project.objects.create(
            user=bid.tailor,  # The tailor who won the bid
            customer=job.customer,
            amount=bid.amount,
            due_date=job.deadline,
            status='not_started',
            notes=f"Accepted bid proposal: {bid.proposal}"
        )

        return Response({
            "message": "Bid accepted and project created!",
            "project_id": project.id
        }, status=status.HTTP_201_CREATED)