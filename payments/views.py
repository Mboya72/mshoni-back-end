from django.shortcuts import render
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .models import EscrowTransaction
from .serializers import EscrowSerializer
from .services import notify_tailor_of_payment

class EscrowViewSet(viewsets.ModelViewSet):
    queryset = EscrowTransaction.objects.all()
    serializer_class = EscrowSerializer

    @action(detail=True, methods=['post'])
    def report_issue(self, request, pk=None):
        escrow = self.get_object()
        escrow.status = 'disputed'
        escrow.save()
        
        # Admin logic can be added here later
        return Response({
            "message": "Transaction paused. Mshoni support will contact you."
        }, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([AllowAny])
def mpesa_callback(request):
    """
    Handles Safaricom Daraja API callbacks.
    """
    stk_callback = request.data.get('Body', {}).get('stkCallback', {})
    result_code = stk_callback.get('ResultCode')
    checkout_id = stk_callback.get('CheckoutRequestID')

    if result_code == 0:  # Success
        try:
            escrow = EscrowTransaction.objects.get(checkout_request_id=checkout_id)
            escrow.status = 'held'
            
            # Extracting Receipt Number safely from Metadata list
            metadata = stk_callback.get('CallbackMetadata', {}).get('Item', [])
            for item in metadata:
                if item.get('Name') == 'MpesaReceiptNumber':
                    escrow.mpesa_receipt_number = item.get('Value')
            
            escrow.save()

            # Update the associated Project
            project = escrow.project
            project.status = 'in_progress' # Or 'paid' depending on your choices
            project.date_downpayment_paid = timezone.now().date()
            project.save()

            # Trigger the automated chat notification
            notify_tailor_of_payment(project)

        except EscrowTransaction.DoesNotExist:
            return Response({"ResultCode": 1, "ResultDesc": "Transaction not found"}, status=status.HTTP_404_NOT_FOUND)
        
    return Response({"ResultCode": 0, "ResultDesc": "Success"})