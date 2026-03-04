from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('tailor', 'Tailor'),
        ('customer', 'Customer'),
        ('admin', 'Admin'),
        ('support', 'Support'),
    )
    
    username = models.CharField(
        max_length=150,
        unique=True,
        null=False,
        blank=False,
    )
    email = models.EmailField(
        unique=True,
        null=False,
        blank=False,
    )
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='CUSTOMER',help_text="Role of the user in the system")
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.role})"