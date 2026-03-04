from django.db import models
from django.conf import settings
# Import from your profiles app instead of a separate customers app
from profiles.models import Profile 

class Order(models.Model):
    CURRENCY_CHOICES = (("USD", "USD"), ("KES", "KES"))
    
    # We use a simple status here, or move this to a separate 'Project' model
    STATUS_CHOICES = (
        ("not_started", "Not started"),
        ("in_progress", "In progress"),
        ("completed", "Completed"),
    )

    # The Tailor/Business owner
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders"
    )
    
    # The Client (Linked to the Profile model we created)
    customer = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="orders",
        limit_choices_to={'role': 'customer'} # Ensures only customers are selected
    )
    
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    downpayment = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        help_text="Amount paid as downpayment",
    )
    currency = models.CharField(max_length=10, choices=CURRENCY_CHOICES, default="KES")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="not_started")
    due_date = models.DateField(help_text="When the order is meant to be delivered")
    notes = models.TextField(blank=True)
    is_fully_paid = models.BooleanField(
        default=False, help_text="Has the full payment been completed?"
    )

    date_downpayment_paid = models.DateField(
        null=True, blank=True, help_text="Date the downpayment was actually paid"
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        # Updated to use the profile username since 'name' might not exist on Profile
        return f"Order for {self.customer.user.username} on {self.date_created.date()}"
    
class ProjectUpdate(models.Model):
    STATUS_CHOICES = (
        ("cutting", "Cutting"),
        ("first_fitting", "First Fitting"),
        ("sewing", "Sewing"),
        ("second_fitting", "Second Fitting"),
        ("finished", "Finished"),
        ("delivered", "Delivered"),
    )
    
    order = models.ForeignKey(
        Order, 
        on_delete=models.CASCADE, 
        related_name="updates"
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    description = models.TextField(blank=True, help_text="What happened in this stage?")
    
    # Optional: Link to an image in your media_file app to show progress
    # image = models.ForeignKey('media_file.MediaFile', on_delete=models.SET_NULL, null=True, blank=True)

    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp'] # Shows newest updates first

    def __str__(self):
        return f"{self.order.id} moved to {self.get_status_display()}"