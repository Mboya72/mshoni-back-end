from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Order
from .serializers import OrderSerializer

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer

    def get_queryset(self):
        user = self.request.user
        if user.role == 'seller':
            # Sellers see orders for their products (Sales Analytics)
            return Order.objects.filter(item__user=user)
        # Tailors/Customers see things they bought
        return Order.objects.filter(buyer=user)

    def perform_create(self, serializer):
        item = serializer.validated_data['item']
        qty = serializer.validated_data['quantity']
        
        # Calculate price based on Seller's set price
        total = item.price_per_yard * qty
        
        # Create the order and decrease seller stock (Inventory Management)
        order = serializer.save(buyer=self.request.user, total_price=total)
        
        item.yards -= qty
        if item.yards <= 0:
            item.is_available = False
        item.save()