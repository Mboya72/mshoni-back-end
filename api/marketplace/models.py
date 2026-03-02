import uuid
from django.db import models

class Service(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tailor = models.ForeignKey("users.TailorProfile", on_delete=models.CASCADE, related_name="services")
    
    name = models.CharField(max_length=255, db_index=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, db_index=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class JobPost(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    customer = models.ForeignKey("users.CustomerProfile", on_delete=models.CASCADE, related_name="job_posts")
    
    title = models.CharField(max_length=255, db_index=True)
    description = models.TextField()
    budget = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    deadline = models.DateField(db_index=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class Bid(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    job = models.ForeignKey(JobPost, on_delete=models.CASCADE, related_name="bids")
    tailor = models.ForeignKey("users.TailorProfile", on_delete=models.CASCADE)
    
    price = models.DecimalField(max_digits=10, decimal_places=2)
    message = models.TextField()
    
    created_at = models.DateTimeField(auto_now_add=True)