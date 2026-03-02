import uuid
from django.db import models

class Project(models.Model):
    STATUS_CHOICES = (
        ("Inquiry", "Inquiry"),
        ("Downpayment_Paid", "Downpayment Paid"),
        ("Cutting", "Cutting"),
        ("Sewing", "Sewing"),
        ("Fitting", "Fitting"),
        ("Ready", "Ready"),
        ("Completed", "Completed"),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    job = models.OneToOneField("marketplace.JobPost", on_delete=models.CASCADE)
    tailor = models.ForeignKey("users.TailorProfile", on_delete=models.CASCADE)
    customer = models.ForeignKey("users.CustomerProfile", on_delete=models.CASCADE)
    
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, db_index=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class Appointment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="appointments")
    scheduled_at = models.DateTimeField(db_index=True)
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
class Appointment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="appointments")
    scheduled_at = models.DateTimeField(db_index=True)
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
class Notification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    user = models.ForeignKey("users.CustomUser", on_delete=models.CASCADE, related_name="notifications")
    title = models.CharField(max_length=255)
    body = models.TextField()
    is_read = models.BooleanField(default=False, db_index=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)