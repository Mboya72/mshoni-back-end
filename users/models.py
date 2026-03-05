from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# 1. Add a Custom Manager to handle email-based creation
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        # Ensure a username exists even if it's just the email prefix
        if not extra_fields.get('username'):
            extra_fields['username'] = email.split('@')[0]
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin') # Sets Mshoni admin role automatically
        return self.create_user(email, password, **extra_fields)

# 2. The User Model
class User(AbstractUser):
    ROLE_CHOICES = (
        ('tailor', 'Tailor'),
        ('customer', 'Customer'),
        ('seller', 'Seller'),
        ('admin', 'Admin'),
        ('support', 'Support'),
    )
    
    profile_picture = models.ForeignKey(
        'media_file.MediaFile',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        default=None,
        related_name='profile_users'
    )

    email = models.EmailField(
        unique=True,
        null=False,
        blank=False,
    )
    
    # Allow null/blank because Google Login users might not have a chosen username yet
    username = models.CharField(
        max_length=150,
        unique=True,
        null=True,
        blank=True
    )
    
    role = models.CharField(
        max_length=20, 
        choices=ROLE_CHOICES, 
        default='customer', 
        help_text="Role of the user in the system"
    )

    date_updated = models.DateTimeField(auto_now=True)

    # Attach the custom manager
    objects = UserManager()

    USERNAME_FIELD = 'email'
    # 'username' must stay in REQUIRED_FIELDS for Django internal compatibility
    REQUIRED_FIELDS = ['username', 'first_name']
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        name = f"{self.first_name} {self.last_name}".strip()
        # Fallback logic: Name > Username > Email
        display = name if name else (self.username if self.username else self.email)
        return f"{display} ({self.get_role_display()})"