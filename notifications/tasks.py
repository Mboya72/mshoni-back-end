# notifications/tasks.py
from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_payment_notification_task(email, amount):
    """
    Task to send an email notification when payment is received.
    This runs in the background.
    """
    subject = 'Payment Received - Mshoni'
    message = f'We have received your payment of {amount} KES and it is now held in Escrow.'
    email_from = 'no-reply@mshoni.com'
    recipient_list = [email]
    
    send_mail(subject, message, email_from, recipient_list)
    return f"Email sent to {email}"