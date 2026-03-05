from celery import shared_task
from django.utils import timezone
from .models import Profile

@shared_task
def check_expired_subscriptions():
    # Find all users whose sub has expired but are still marked as PRO/PREMIUM
    expired_profiles = Profile.objects.filter(
        subscription_expires__lt=timezone.now(),
        membership_tier__in=['PRO', 'PREMIUM']
    )
    
    count = expired_profiles.count()
    for profile in expired_profiles:
        profile.membership_tier = 'FREE'
        profile.save()
        # PRO TIP: Send a notification here using your existing notification task
        # send_payment_notification_task.delay(profile.user.email, "Your subscription has expired.")

    return f"Demoted {count} expired subscriptions."