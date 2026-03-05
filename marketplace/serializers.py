from rest_framework import serializers
from .models import Order
from .models import JobPost, Bid
from profiles.serializers import ProfileSerializer

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
    
class BidSerializer(serializers.ModelSerializer):
    tailor_name = serializers.ReadOnlyField(source='tailor.username')
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Bid
        fields = [
            'id', 'job', 'tailor', 'tailor_name', 'amount', 
            'proposal', 'estimated_days', 'status', 'status_display', 'created_at'
        ]
        read_only_fields = ['tailor', 'status']

class JobPostSerializer(serializers.ModelSerializer):
    # This allows a customer to see all bids on their post
    bids = BidSerializer(many=True, read_only=True)
    customer_details = ProfileSerializer(source='customer', read_only=True)
    bid_count = serializers.IntegerField(source='bids.count', read_only=True)

    class Meta:
        model = JobPost
        fields = [
            'id', 'customer', 'customer_details', 'title', 'description', 
            'budget_range', 'category', 'deadline', 'reference_image', 
            'is_active', 'bid_count', 'bids', 'created_at'
        ]
        read_only_fields = ['customer', 'is_active']