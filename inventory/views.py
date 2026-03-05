from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Inventory
from .serializers import InventorySerializer

class InventoryViewSet(viewsets.ModelViewSet):
    serializer_class = InventorySerializer
    permission_classes = [IsAuthenticated]

    # This ensures users only see their OWN inventory items
    def get_queryset(self):
        return Inventory.objects.filter(user=self.request.user)

    # This automatically saves the user who created the item
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)