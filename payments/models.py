from django.db import models
from django.conf import settings
# Import Project from your projects app
from projects.models import Project 

class EscrowTransaction(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Payment'),
        ('held', 'Funds Held in Escrow'),
        ('disputed', 'Disputed'),
        ('released', 'Released to Tailor/Seller'),
        ('refunded', 'Refunded to Customer'),
    ]

    # Link to Project instead of Order
    project = models.OneToOneField(
        Project, 
        on_delete=models.CASCADE, 
        related_name='escrow_details'
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    commission_fee = models.DecimalField(max_digits=10, decimal_places=2)
    
    checkout_request_id = models.CharField(max_length=100, blank=True, null=True)
    mpesa_receipt_number = models.CharField(max_length=50, blank=True, null=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Escrow for Project {self.project.id} - {self.status}"