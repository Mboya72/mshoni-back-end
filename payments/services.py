# payments/services.py (Business Logic)
from django.utils import timezone

def release_funds(escrow_id):
    """Transfer funds from Mshoni holding account to the Tailor's M-Pesa"""
    escrow = EscrowTransaction.objects.get(id=escrow_id)
    
    if escrow.status == 'held':
        # 1. Calculate Payout (Amount - Commission)
        payout_amount = escrow.amount - escrow.commission_fee
        
        # 2. Trigger M-Pesa B2C (Business to Customer) API call here
        # success = mpesa_b2c_transfer(escrow.order.tailor.phone, payout_amount)
        
        escrow.status = 'released'
        escrow.save()
        return True
    return False

def initiate_dispute(escrow_id):
    """Pause the transaction so the Admin can investigate"""
    escrow = EscrowTransaction.objects.get(id=escrow_id)
    escrow.status = 'disputed'
    escrow.save()
    # Trigger an email/notification to you (the Admin)