from django.db import models
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField

class Profile(models.Model):
    ROLE_CHOICES = [
        ('tailor', 'Tailor'),
        ('customer', 'Customer'),
        ('admin', 'Admin'),
        ('support', 'Support'),
    ]
    TAILOR_TYPE_CHOICES = [
        ('regular', 'Regular Tailor'),
        ('bespoke', 'Bespoke Tailor (Subscribed)'),
    ]

    # --- Core Fields ---
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name="profile"
    )
    # Keeping role here is fine for quick profile lookups, but ensure it matches User.role
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    
    tailor_type = models.CharField(
        max_length=20, 
        choices=TAILOR_TYPE_CHOICES, 
        default='regular',
        help_text="Only applicable for users with the 'tailor' role."
    )
    phone_number = PhoneNumberField(blank=True)
    address = models.CharField(max_length=255, blank=True)

    # REMOVED: profile_picture. 
    # Why? Because you added it as a ForeignKey to MediaFile in your User model.
    # Access it via: request.user.profile_picture

    # --- Customer Specific Data ---
    measurements = models.JSONField(default=dict, blank=True) 
    measurement_unit = models.CharField(max_length=10, default="metric")

    # --- Tailor Specific Data ---
    business_name = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True)
    experience_years = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"

class CatalogueItem(models.Model):
    # Fixed: Use string reference 'media.MediaFile' to match your app name 'media'
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="catalogue_items",
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    
    category = models.CharField(
        max_length=100, 
        help_text="e.g. Bridal, Men's Suit", 
        blank=True
    )
    
    starting_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True
    )
    
    # Updated: Changed app name to 'media' to match your User model import
    cover_image = models.ForeignKey(
        'media_file.MediaFile', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name="catalogue_covers"
    )

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} by {self.user.username}"