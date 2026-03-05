from django.db import models
from django.conf import settings
from inventory.models import Inventory

class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending Payment'),
        ('escrow', 'Payment in Escrow'), # Matches your Escrow requirement
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )

    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='purchases')
    item = models.ForeignKey(Inventory, on_delete=models.CASCADE, related_name='sales')
    quantity = models.FloatField()
    total_price = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # For Delivery & Logistics requirement
    delivery_method = models.CharField(max_length=50, default='pickup') # pickup or courier
    tracking_number = models.CharField(max_length=100, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Review(models.Model):
    """Addresses the Reviews & Ratings System requirement"""
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='review')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(default=5) # 1 to 5
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)