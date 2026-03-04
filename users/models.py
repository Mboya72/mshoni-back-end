from django.db import models
from django.contrib.auth.models import AbstractUser
# Remove the direct import of MediaFile to avoid circular imports

class User(AbstractUser):
    ROLE_CHOICES = (
        ('tailor', 'Tailor'),
        ('customer', 'Customer'),
        ('admin', 'Admin'),
        ('support', 'Support'),
    )
    
    # Use the string 'media.MediaFile' instead of the class name
    profile_picture = models.ForeignKey(
        'media.MediaFile', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        default=None,  # Add this line explicitly
        related_name='profile_users'
    )

    email = models.EmailField(
        unique=True,
        null=False,
        blank=False,
    )
    
    role = models.CharField(
        max_length=20, 
        choices=ROLE_CHOICES, 
        default='customer', 
        help_text="Role of the user in the system"
    )

    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        name = f"{self.first_name} {self.last_name}".strip()
        return f"{name if name else self.username} ({self.get_role_display()})"