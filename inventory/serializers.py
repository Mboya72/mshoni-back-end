from rest_framework import serializers
from .models import Inventory

class InventorySerializer(serializers.ModelSerializer):
    # We make 'user' read-only so the system automatically 
    # assigns the logged-in user as the owner.
    user = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = Inventory
        fields = '__all__'