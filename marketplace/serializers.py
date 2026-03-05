from rest_framework import serializers
from .models import Order
from inventory.serializers import InventorySerializer

class OrderSerializer(serializers.ModelSerializer):
    item_details = InventorySerializer(source='item', read_only=True)
    buyer_email = serializers.ReadOnlyField(source='buyer.email')

    class Order:
        model = Order
        fields = ['id', 'buyer_email', 'item', 'item_details', 'quantity', 'total_price', 'status', 'created_at']
        read_only_fields = ['total_price', 'status']

    def validate(self, data):
        # Ensure the seller isn't buying their own item
        if data['item'].user == self.context['request'].user:
            raise serializers.ValidationError("You cannot buy your own inventory.")
        # Ensure enough stock
        if data['quantity'] > data['item'].yards:
            raise serializers.ValidationError(f"Only {data['item'].yards} yards available.")
        return data