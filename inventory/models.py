from django.db import models
from django.conf import settings

class Inventory(models.Model):
    MATERIAL_TYPES = [
        ('fabric', 'Fabric'),
        ('tool', 'Sewing Equipment'),
        ('thread', 'Threads/Buttons'),
        ('accessory', 'Bags/Belts/Finished Acc'),
    ]

    UNIT_CHOICES = [
        ('yards', 'Yards'),
        ('pieces', 'Pieces/Units'),
        ('meters', 'Meters'),
    ]

    # Who is selling this? (Tailor or Material Seller)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name="inventory"
    )
    
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=20, choices=MATERIAL_TYPES, default='fabric')
    description = models.TextField(blank=True)
    
    # --- Pricing & Quantity Logic ---
    unit_type = models.CharField(max_length=10, choices=UNIT_CHOICES, default='yards')
    quantity = models.FloatField(help_text="Available amount (yards, pieces, etc.)")
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    # New fields with defaults to satisfy migrations
    unit_type = models.CharField(
        max_length=10, 
        choices=[('yard', 'Yard'), ('piece', 'Piece')], 
        default='yard'
    )
    quantity = models.FloatField(
        default=0.0, 
        help_text="Available amount (yards, pieces, etc.)"
    )
    
    # --- Visuals (Linking to your MediaFile app) ---
    # Assuming your app is named 'media_file' and model is 'MediaFile'
    image = models.ForeignKey(
        'media_file.MediaFile', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name="inventory_images"
    )
    
    # --- Status & Tier Logic ---
    is_available = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False, help_text="Set to True for Premium/Pro sellers")
    
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Inventory Items"
        ordering = ['-is_featured', '-date_created'] # Premium items appear first

    def __str__(self):
        return f"{self.name} ({self.quantity} {self.unit_type})"

    @property
    def total_value(self):
        return self.quantity * self.price_per_unit