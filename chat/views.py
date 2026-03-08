from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .models import Message, Conversation
from .serializers import MessageSerializer, ConversationSerializer # Ensure these exist!

# 1. Conversation ViewSet
class ConversationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer

    def get_queryset(self):
        # Filter: Only show conversations where the logged-in user is a participant
        return self.queryset.filter(participants=self.request.user)

# 2. Fixed Inbox List (The /api/chat/threads/ endpoint)
class ChatThreadListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ConversationSerializer

    def get_queryset(self):
        # FIX: Changed 'order_index' to 'order_by'
        # This sorts the most recent messages to the top of the Flutter list
        return Conversation.objects.filter(
            participants=self.request.user
        ).order_by('-updated_at')

# 3. Message Actions
class MessageViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    @action(detail=True, methods=['post'])
    def acknowledge_receipt(self, request, pk=None):
        message = self.get_object()
        # Only update if it hasn't been marked delivered yet
        if not message.is_delivered:
            message.is_delivered = True
            message.delivered_at = timezone.now()
            message.save()
        return Response({'status': 'delivered'})

    @action(detail=True, methods=['post'])
    def mark_seen(self, request, pk=None):
        message = self.get_object()
        # Logic: Only mark as seen if the reader is NOT the sender
        if message.sender != request.user and not message.is_seen:
            message.is_seen = True
            message.seen_at = timezone.now()
            message.save()
        return Response({'status': 'read'})