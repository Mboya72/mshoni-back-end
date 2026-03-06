from decimal import Decimal
from django.db.models import Sum
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

# Import your models
from .models import Bid, JobPost, Order

class MarketplaceStatsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        # Logic check: Using user.role (from Google Login) or profile.role
        role = getattr(user, 'role', 'customer')
        is_tailor = role == 'tailor'

        if is_tailor:
            # Stats for the Tailor (Seller/Service Provider)
            sales_data = Order.objects.filter(item__user=user).aggregate(Sum('total_price'))
            total_sales = sales_data['total_price__sum'] or 0
            active_bids = Bid.objects.filter(tailor=user, status='pending').count()
            total_orders = Order.objects.filter(item__user=user).count()
            
            return Response({
                "total_revenue": total_sales,
                "active_bids": active_bids,
                "orders_count": total_orders,
                "role": "tailor"
            })
        else:
            # Stats for the Customer (Buyer)
            spent_data = Order.objects.filter(buyer=user).aggregate(Sum('total_price'))
            total_spent = spent_data['total_price__sum'] or 0
            active_jobs = JobPost.objects.filter(customer__user=user, is_active=True).count()
            my_orders = Order.objects.filter(buyer=user).count()

            return Response({
                "total_spent": total_spent,
                "active_jobs": active_jobs,
                "orders_placed": my_orders,
                "role": "customer"
            })

class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    # serializer_class = OrderSerializer # Ensure this is imported correctly

    def get_queryset(self):
        user = self.request.user
        # Standardizing on user.role for Mshoni
        if getattr(user, 'role', 'customer') == 'tailor':
            return Order.objects.filter(item__user=user)
        return Order.objects.filter(buyer=user)

    def perform_create(self, serializer):
        item = serializer.validated_data['item']
        qty = Decimal(str(serializer.validated_data['quantity']))
        
        # Calculate price based on Inventory pricing
        total = Decimal(str(item.price_per_yard)) * qty
        
        # Save order and update inventory
        order = serializer.save(buyer=self.request.user, total_price=total)
        
        item.yards -= float(qty)
        if item.yards <= 0:
            item.yards = 0
            item.is_available = False
        item.save()

class BidViewSet(viewsets.ModelViewSet):
    queryset = Bid.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    # serializer_class = BidSerializer

    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        bid = self.get_object()
        job = bid.job

        if job.customer.user != request.user:
            return Response({"error": "Unauthorized."}, status=status.HTTP_403_FORBIDDEN)

        bid.status = 'accepted'
        bid.save()
        job.is_active = False
        job.save()

        # Import here to avoid circular dependencies
        from projects.models import Project
        project = Project.objects.create(
            user=bid.tailor,
            customer=job.customer,
            amount=bid.amount,
            due_date=job.deadline,
            status='not_started',
            notes=f"Accepted bid proposal: {bid.proposal}"
        )

        return Response({
            "message": "Bid accepted!",
            "project_id": project.id
        }, status=status.HTTP_201_CREATED)