from rest_framework import serializers
from .models import Order

class OrderSerializer(serializers.ModelSerializer):
    # These fields are calculated on the backend, so they are read-only for the user
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    buyer_username = serializers.ReadOnlyField(source='buyer.username')
    item_name = serializers.ReadOnlyField(source='item.name') # Assuming your material model has a name

    class Meta:
        model = Order
        fields = [
            'id', 'item', 'item_name', 'buyer', 'buyer_username', 
            'quantity', 'total_price', 'status', 'created_at'
        ]
        read_only_fields = ['buyer', 'status']

    def validate_quantity(self, value):
        """
        Check that the requested quantity is actually available in stock.
        """
        # We access the item from the initial data since it's not yet validated
        item_id = self.initial_data.get('item')
        from .models import Material # Replace with your actual material/item model name
        
        try:
            item = Material.objects.get(id=item_id)
            if value > item.yards:
                raise serializers.ValidationError(
                    f"Only {item.yards} yards available in stock."
                )
        except Material.DoesNotExist:
            raise serializers.ValidationError("Item not found.")
            
        return value