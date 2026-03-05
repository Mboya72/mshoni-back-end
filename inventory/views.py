# inventory/views.py
from rest_framework import viewsets, permissions
from .models import Inventory
from .serializers import InventorySerializer
from .permissions import IsSeller # Import your new permission

class InventoryViewSet(viewsets.ModelViewSet):
    serializer_class = InventorySerializer

    def get_permissions(self):
        # Anyone authenticated can view (GET)
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        # Only Sellers can create, update, or delete
        return [IsSeller()]

    def get_queryset(self):
        # Sellers see their own stock management
        if self.request.user.role == 'seller':
            return Inventory.objects.filter(user=self.request.user)
        # Tailors see all available materials to purchase
        return Inventory.objects.filter(is_available=True)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)