from django.db import models
from django.conf import settings
# Keep your MediaFile import if you are using it for a Generic Relation 
# or a specific ForeignKey

class Inventory(models.Model):
    MATERIAL_TYPES = [
        ('fabric', 'Fabric'),
        ('tool', 'Sewing Equipment'),
        ('thread', 'Threads/Buttons'),
    ]

    # Who is selling this? (Tailor or Material Seller)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="inventory"
    )
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=20, choices=MATERIAL_TYPES, default='fabric')
    description = models.TextField(blank=True)
    
    # Pricing & Quantity
    yards = models.FloatField(help_text="Available length in yards")
    price_per_yard = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    image = models.ImageField(upload_to='inventory/', null=True, blank=True)
    # Status tracking (Important for "Sold Fabrics" feature)
    is_available = models.BooleanField(default=True)
    
    # Media linkage (Example of how to use your import)
    # If using a standard ForeignKey for a single main image:
    # image = models.ForeignKey(MediaFile, on_delete=models.SET_NULL, null=True, blank=True)

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.yards} yds)"