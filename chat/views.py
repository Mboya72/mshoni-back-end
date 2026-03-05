# chat/views.py
from django.utils import timezone
from rest_framework.decorators import action

class MessageViewSet(viewsets.ModelViewSet):
    # ... previous setup ...

    @action(detail=True, methods=['post'])
    def acknowledge_receipt(self, request, pk=None):
        """Standard 'Delivered' check"""
        message = self.get_object()
        message.is_delivered = True
        message.delivered_at = timezone.now()
        message.save()
        
        # Broadcast the 'Delivered' status back to the Sender via WebSocket
        # (This triggers the double-grey tick in WhatsApp)
        return Response({'status': 'delivered'})

    @action(detail=True, methods=['post'])
    def mark_seen(self, request, pk=None):
        """Standard 'Read' check (The Blue Ticks)"""
        message = self.get_object()
        message.is_seen = True
        message.seen_at = timezone.now()
        message.save()
        
        return Response({'status': 'read'})