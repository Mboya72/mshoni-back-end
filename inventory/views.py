from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, PermissionDenied
from .models import Inventory
from .serializers import InventorySerializer

class InventoryViewSet(viewsets.ModelViewSet):
    serializer_class = InventorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    # This ensures Premium items and newest items are always first
    ordering = ['-is_featured', '-date_created'] 

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and self.request.query_params.get('my_items'):
            # Using .order_by here ensures the 'Featured' logic applies
            return Inventory.objects.filter(user=user).order_by('-date_created')
        
        return Inventory.objects.filter(is_available=True).order_by('-is_featured', '-date_created')

    def perform_create(self, serializer):
        user = self.request.user
        profile = user.profile
        current_count = user.inventory.count()

        # --- Mshoni Tier Enforcement ---
        # Free users: 5 items limit
        if profile.membership_tier == 'FREE' and current_count >= 5:
            raise ValidationError({
                "limit_reached": "Free accounts are limited to 5 inventory items. Upgrade to PRO to list more!"
            })

        # Automatic "Featured" status for Premium/Pro users
        is_featured = (profile.membership_tier in ['PRO', 'PREMIUM'])
        
        serializer.save(user=user, is_featured=is_featured)

    def perform_update(self, serializer):
        # Security: Only the owner can edit their inventory
        if serializer.instance.user != self.request.user:
            raise PermissionDenied("You do not have permission to edit this item.")
        serializer.save()