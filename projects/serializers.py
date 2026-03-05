from rest_framework import serializers
from .models import Project, ProjectUpdate
from payments.serializers import EscrowSerializer

class ProjectUpdateSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = ProjectUpdate
        fields = ['id', 'status', 'status_display', 'description', 'image', 'timestamp']

class ProjectSerializer(serializers.ModelSerializer):
    # Nesting the escrow data
    escrow = EscrowSerializer(read_only=True)
    # Including the timeline of updates
    updates = ProjectUpdateSerializer(many=True, read_only=True)
    
    customer_name = serializers.ReadOnlyField(source='customer.user.username')
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Project
        fields = [
            'id', 'user', 'customer', 'customer_name', 'amount', 
            'downpayment', 'currency', 'status', 'status_display', 
            'due_date', 'is_fully_paid', 'escrow', 'updates', 'notes'
        ]