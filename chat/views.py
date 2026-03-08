from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils import timezone
from .models import Message

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    # serializer_class = MessageSerializer

    @action(detail=True, methods=['post'])
    def acknowledge_receipt(self, request, pk=None):
        message = self.get_object()
        
        # Only update if not already delivered
        if not message.is_delivered:
            message.is_delivered = True
            message.delivered_at = timezone.now()
            message.save()
        
        return Response({'status': 'delivered'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def mark_seen(self, request, pk=None):
        message = self.get_object()
        
        # Logic: You shouldn't be able to "read" your own message to trigger blue ticks
        if message.sender != request.user and not message.is_seen:
            message.is_seen = True
            message.seen_at = timezone.now()
            message.save()
            
            # TODO: Trigger your WebSocket layer here to notify the sender
            
        return Response({'status': 'read'}, status=status.HTTP_200_OK)