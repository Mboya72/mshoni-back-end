from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        TAILOR = "TAILOR", "Tailor"
        CUSTOMER = "CUSTOMER", "Customer"

    role = models.CharField(
        max_length=10, 
        choices=Role.choices, 
        default=Role.CUSTOMER
    )
    # Shared field for all users
    phone_number = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return f"{self.username} ({self.role})"

class TailorProfile(models.Model):
    # Links to the User model
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='tailor_profile')
    shop_name = models.CharField(max_length=255)
    bio = models.TextField(blank=True)

    def __str__(self):
        return f"Tailor: {self.shop_name}"

class CustomerProfile(models.Model):
    # Links to the User model
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer_profile')
    address = models.TextField(blank=True)
    chest_size = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"Customer: {self.user.username}"