from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User
from profiles.models import Profile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(
            user=instance, 
            role=instance.role
        )

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    # This ensures if you change the role on the User, it updates the Profile too
    if hasattr(instance, 'profile'):
        instance.profile.role = instance.role
        instance.profile.save()