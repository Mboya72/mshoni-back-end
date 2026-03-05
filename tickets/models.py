from django.db import models
from django.conf import settings

class Ticket(models.Model):
    # Added categories to match your Mshoni features list
    CATEGORY_CHOICES = [
        ('payment', 'Payment & Escrow'),
        ('project', 'Project/Tailoring Dispute'),
        ('order', 'Material/Seller Order'),
        ('account', 'Account & Subscription'),
        ('technical', 'App Technical Issue'),
    ]

    STATUS_CHOICES = [
        ('open', 'Open'),
        ('pending', 'Pending'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent (Pro/Premium)'), # Added for priority support
    ]

    # Core Relationships
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name="tickets"
    )
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name="assigned_tickets",
        limit_choices_to={'is_staff': True} # Only Support/Admins can be assigned
    )
    
    # Mshoni Specific Context
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='technical')
    subject = models.CharField(max_length=255)
    description = models.TextField()
    
    # Link to Project or Seller Order for dispute resolution
    project = models.ForeignKey(
        'projects.Project', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name="dispute_tickets"
    )
    # If you have a separate Order model for materials/fabrics:
    # order = models.ForeignKey('orders.Order', on_delete=models.SET_NULL, null=True, blank=True)

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='open')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    
    # Audit Trail
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date_created'] # Newest tickets first in Admin

    def __str__(self):
        return f"[{self.category.upper()}] #{self.id} - {self.subject}"