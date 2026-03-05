from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Order # Assuming Order still exists for fabric sales
from .serializers import OrderSerializer

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