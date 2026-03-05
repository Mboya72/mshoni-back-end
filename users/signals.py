from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User
from profiles.models import Profile

@receiver(post_save, sender=User)
def manage_user_profile(sender, instance, created, **kwargs):
    """
    Handles both creation and role synchronization in a single optimized receiver.
    """
    if created:
        # Create profile only if it doesn't exist (important for social logins)
        Profile.objects.get_or_create(
            user=instance, 
            defaults={'role': instance.role}
        )
    else:
        # Sync role from User to Profile only if it has changed
        # We use update() to avoid triggering the Profile's post_save signals again
        Profile.objects.filter(user=instance).exclude(role=instance.role).update(role=instance.role)

# Optional: Ensure the profile is saved if other non-role fields change
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, created, **kwargs):
    if not created:
        if hasattr(instance, 'profile'):
            instance.profile.save()