from django.db import models
from django.conf import settings

class Conversation(models.Model):
    """A thread between two users (e.g., Tailor & Seller)"""
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Conversation between {', '.join([u.username for u in self.participants.all()])}"

# chat/models.py
class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField(blank=True)
    image = models.ImageField(upload_to='chat_images/', null=True, blank=True)
    is_read = models.BooleanField(default=False)
    
    # ENSURE THIS FIELD EXISTS:
    created_at = models.DateTimeField(auto_now_add=True) 

    # WhatsApp-style status fields we added earlier
    is_delivered = models.BooleanField(default=False)
    is_seen = models.BooleanField(default=False)

    class Meta:
        # This is the line that was causing the error
        ordering = ['created_at'] 

    def __str__(self):
        return f"Message from {self.sender.email} at {self.created_at}"
    class Meta:
        ordering = ['created_at']