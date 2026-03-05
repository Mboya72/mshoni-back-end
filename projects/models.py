from django.db import models
from django.conf import settings

class Project(models.Model):  # Renamed from Order to Project
    CURRENCY_CHOICES = (("USD", "USD"), ("KES", "KES"))
    
    STATUS_CHOICES = (
        ("not_started", "Not started"),
        ("in_progress", "In progress"),
        ("completed", "Completed"),
    )

    # The Tailor/Business owner
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="projects"
    )
    
    # Using string reference 'profiles.Profile' to prevent import crashes
    customer = models.ForeignKey(
        'profiles.Profile', 
        on_delete=models.CASCADE, 
        related_name="projects",
        limit_choices_to={'role': 'customer'}
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
    due_date = models.DateField(help_text="When the work is meant to be delivered")
    notes = models.TextField(blank=True)
    is_fully_paid = models.BooleanField(
        default=False, help_text="Has the full payment been completed?"
    )

    date_downpayment_paid = models.DateField(
        null=True, blank=True, help_text="Date the downpayment was actually paid"
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    
    escrow = models.OneToOneField(
    'payments.EscrowTransaction', 
    on_delete=models.SET_NULL, 
    null=True, 
    blank=True,
    related_name='tailor_project'
    )

    def __str__(self):
        return f"Project for {self.customer.user.username} - {self.status}"

class ProjectUpdate(models.Model):
    STATUS_CHOICES = (
        ("cutting", "Cutting"),
        ("first_fitting", "First Fitting"),
        ("sewing", "Sewing"),
        ("second_fitting", "Second Fitting"),
        ("finished", "Finished"),
        ("delivered", "Delivered"),
    )
    
    project = models.ForeignKey(
        Project, # Now links to the renamed Project model
        on_delete=models.CASCADE, 
        related_name="updates"
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    description = models.TextField(blank=True)
    
    # Corrected string reference for your media app
    image = models.ForeignKey(
        'media_file.MediaFile', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )

    timestamp = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Determine if this is a new update or an edit
        is_new = self._state.adding 
        super().save(*args, **kwargs)
        
        # Trigger parent status change only when 'finished' is set
        if self.status == 'finished':
            self.project.status = 'completed'
            self.project.save()

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"Update: {self.project.id} is now {self.get_status_display()}"
    