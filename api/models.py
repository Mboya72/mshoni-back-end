from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.core.validators import MinValueValidator

# --- AUTH & USERS ---

class User(AbstractUser):
    ROLE_CHOICES = (
        ('TAILOR', 'Tailor'),
        ('CUSTOMER', 'Customer'),
        ('SELLER', 'Material Seller'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    phone_number = models.CharField(max_length=20, blank=True)
    whatsapp_enabled = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

# --- PROFILES ---

class TailorProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tailor_profile')
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=255, blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    
    def __str__(self):
        return f"Tailor: {self.user.username}"

class CustomerProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='customer_profile')
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=255, blank=True)
    preferences = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return f"Customer: {self.user.username}"

class SellerProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='seller_profile')
    shop_name = models.CharField(max_length=255)
    address = models.TextField(blank=True)

    def __str__(self):
        return f"Seller: {self.shop_name}"

# --- TAILOR SERVICES ---

class ServiceMenu(models.Model):
    tailor = models.ForeignKey(TailorProfile, on_delete=models.CASCADE, related_name='services')
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    estimated_days = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.name} - {self.tailor.user.username}"

class LookbookItem(models.Model):
    tailor = models.ForeignKey(TailorProfile, on_delete=models.CASCADE, related_name='lookbook')
    image = models.ImageField(upload_to='lookbooks/')
    description = models.TextField(blank=True)
    style_category = models.CharField(max_length=50)

# --- JOBS & BIDDING ---

class JobPost(models.Model):
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posted_jobs')
    title = models.CharField(max_length=200)
    description = models.TextField()
    is_open_for_bidding = models.BooleanField(default=True)
    budget = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Bid(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('ACCEPTED', 'Accepted'),
        ('REJECTED', 'Rejected'),
    )
    job = models.ForeignKey(JobPost, on_delete=models.CASCADE, related_name='bids')
    tailor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='my_bids')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    proposal = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')

# --- PROJECTS & TRACKING ---

class Project(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('CUTTING', 'Cutting'),
        ('SEWING', 'Sewing'),
        ('FITTING', 'Fitting'),
        ('FINISHED', 'Finished'),
        ('DELIVERED', 'Delivered'),
    )
    job = models.OneToOneField(JobPost, on_delete=models.SET_NULL, null=True, blank=True)
    tailor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tailor_projects')
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='customer_projects')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    measurements_used = models.TextField()
    due_date = models.DateField(null=True, blank=True)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)

# --- INVENTORY & MARKETPLACE ---

class Material(models.Model):
    seller = models.ForeignKey(SellerProfile, on_delete=models.CASCADE, related_name='inventory')
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.IntegerField(default=0)
    image = models.ImageField(upload_to='materials/', blank=True)

    def __str__(self):
        return self.name

# --- COMMUNICATION & APPOINTMENTS ---

class Appointment(models.Model):
    tailor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tailor_appointments')
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='customer_appointments')
    date_time = models.DateTimeField()
    location = models.CharField(max_length=255)
    notes = models.TextField(blank=True)

class Measurement(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='saved_measurements')
    label = models.CharField(max_length=100)
    data = models.JSONField()

class Message(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
class Tag(models.Model):
    tailor = models.ForeignKey(TailorProfile, on_delete=models.CASCADE, related_name='tags')
    # Using settings.AUTH_USER_MODEL for best practice
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='customer_tags')
    label = models.CharField(max_length=100)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.label} - {self.customer.username}"

class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user.username}"