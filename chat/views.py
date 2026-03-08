from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .models import Message, Conversation # Ensure these models exist
# from .serializers import MessageSerializer, ConversationSerializer 

# 1. The Missing ViewSet that caused the crash
class ConversationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Conversation.objects.all()
    # serializer_class = ConversationSerializer

    def get_queryset(self):
        # Only show conversations the user is part of
        return self.queryset.filter(participants=self.request.user)

# 2. The ListView for your "Inbox"
class ChatThreadListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    # serializer_class = ConversationSerializer

    def get_queryset(self):
        return Conversation.objects.filter(participants=self.request.user).order_index('-updated_at')

# 3. Message Actions (Receipts/Seen)
class MessageViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Message.objects.all()

    @action(detail=True, methods=['post'])
    def acknowledge_receipt(self, request, pk=None):
        message = self.get_object()
        if not message.is_delivered:
            message.is_delivered = True
            message.delivered_at = timezone.now()
            message.save()
        return Response({'status': 'delivered'})

    @action(detail=True, methods=['post'])
    def mark_seen(self, request, pk=None):
        message = self.get_object()
        if message.sender != request.user and not message.is_seen:
            message.is_seen = True
            message.seen_at = timezone.now()
            message.save()
        return Response({'status': 'read'})