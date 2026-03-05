from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import EscrowTransaction
from .serializers import EscrowSerializer # Assuming you created this

class EscrowViewSet(viewsets.ModelViewSet):
    queryset = EscrowTransaction.objects.all()
    serializer_class = EscrowSerializer

    # ... other methods ...

    @action(detail=True, methods=['post'])
    def report_issue(self, request, pk=None):
        escrow = self.get_object()
        escrow.status = 'disputed'
        escrow.save()
        
        # This is where you'll eventually hook in your 
        # Support/Admin notification logic
        
        return Response({
            "message": "Transaction paused. Mshoni support will contact you."
        }, status=status.HTTP_200_OK)

# payments/views.py
@api_view(['POST'])
@permission_classes([AllowAny]) # Safaricom doesn't send Auth headers
def mpesa_callback(request):
    data = request.data.get('Body').get('stkCallback')
    result_code = data.get('ResultCode')
    checkout_id = data.get('CheckoutRequestID')

    if result_code == 0: # Success
        escrow = EscrowTransaction.objects.get(checkout_request_id=checkout_id)
        escrow.status = 'held'
        escrow.mpesa_receipt_number = data.get('CallbackMetadata').get('Item')[1].get('Value')
        escrow.save()
        
        # Update the Order status too
        escrow.order.status = 'paid_and_processing'
        escrow.order.save()
        
    return Response({"ResultCode": 0, "ResultDesc": "Success"})