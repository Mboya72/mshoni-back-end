from django.db import models
from django.conf import settings
from inventory.models import Inventory

# 1. JobPost Model (The "Request" a customer makes)
class JobPost(models.Model):
    customer = models.ForeignKey('profiles.Profile', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    deadline = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# 2. Bid Model (The "Offer" a tailor makes)
class Bid(models.Model):
    job = models.ForeignKey(JobPost, on_delete=models.CASCADE, related_name='bids')
    tailor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    proposal = models.TextField()
    status = models.CharField(max_length=20, default='pending') # pending, accepted, rejected
    created_at = models.DateTimeField(auto_now_add=True)

# 3. Order Model (Purchasing Inventory/Fabric)
class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending Payment'),
        ('escrow', 'Payment in Escrow'),
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
    
    # Delivery & Logistics
    delivery_method = models.CharField(max_length=50, default='pickup') 
    tracking_number = models.CharField(max_length=100, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# 4. Review Model
class Review(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='review')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(default=5) 
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)