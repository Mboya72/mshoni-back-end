from rest_framework import serializers
from .models import Inventory

class InventorySerializer(serializers.ModelSerializer):
    # Display the owner's email and their membership tier for the Marketplace UI
    user_email = serializers.ReadOnlyField(source='user.email')
    membership_tier = serializers.ReadOnlyField(source='user.profile.membership_tier')
    
    # Calculate the total value of the stock automatically for the Admin/Seller view
    total_stock_value = serializers.ReadOnlyField(source='total_value')

    class Meta:
        model = Inventory
        fields = [
            'id', 'user_email', 'membership_tier', 'name', 'category', 
            'description', 'unit_type', 'quantity', 'price_per_unit', 
            'total_stock_value', 'image', 'is_available', 'is_featured', 
            'date_created'
        ]
        # Protect these fields so users can't "hack" their way into Premium features
        read_only_fields = ('id', 'user_email', 'membership_tier', 'is_featured', 'date_created')

    def validate_quantity(self, value):
        if value < 0:
            raise serializers.ValidationError("Quantity cannot be negative.")
        return value