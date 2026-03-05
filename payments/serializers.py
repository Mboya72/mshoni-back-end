from rest_framework import serializers
from .models import EscrowTransaction

class EscrowSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = EscrowTransaction
        fields = [
            'id', 'amount', 'commission_fee', 'status', 
            'status_display', 'mpesa_receipt_number', 'created_at'
        ]
        read_only_fields = ['status', 'mpesa_receipt_number']