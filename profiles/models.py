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

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    phone_number = PhoneNumberField(blank=True)
    address = models.CharField(max_length=255, blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True)

    # --- Customer Specific Data ---
    measurements = models.JSONField(default=dict, blank=True) 
    measurement_unit = models.CharField(max_length=10, default="metric")

    # --- Tailor Specific Data ---
    business_name = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True)
    experience_years = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} - {self.role}"