from django.db import models
from django.conf import settings


class MediaFile(models.Model):
    FILE_TYPES = (
        ('image', 'Image'),
        ('video', 'Video'),
        ('pdf', 'PDF/Document'),
    )

    url = models.URLField(max_length=500) # Increased length for long cloud URLs
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name="uploaded_media"
    )
    file_type = models.CharField(max_length=10, choices=FILE_TYPES, default='image')
    
    # Helpful for the Flutter app to know what the image is for
    description = models.CharField(max_length=255, blank=True) 

    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file_type} - {self.url[:30]}..."