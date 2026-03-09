from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication # Add this
from django.utils import timezone
from .models import Message, Conversation
from .serializers import MessageSerializer, ConversationSerializer

# 1. Conversation ViewSet (For Detail views / Chat Windows)
class ConversationViewSet(viewsets.ModelViewSet):
    # Explicitly define JWT to bypass any Session/CSRF issues
    authentication_classes = [JWTAuthentication] 
    permission_classes = [IsAuthenticated]
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer

    def get_queryset(self):
        # Filter: Only show conversations where the logged-in user is a participant
        return self.queryset.filter(participants=self.request.user)

# 2. Inbox List (The /api/chat/threads/ endpoint)
class ChatThreadListView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication] # Crucial for Flutter
    permission_classes = [IsAuthenticated]
    serializer_class = ConversationSerializer

    def get_queryset(self):
        # Optimized: prefetch_related reduces database hits for 'participants'
        return Conversation.objects.filter(
            participants=self.request.user
        ).prefetch_related('participants').order_by('-updated_at')

# 3. Message Actions (For Receipt/Seen logic)
class MessageViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    @action(detail=True, methods=['post'])
    def acknowledge_receipt(self, request, pk=None):
        message = self.get_object()
        # Security: Only recipient should be able to mark as delivered
        if not message.is_delivered:
            message.is_delivered = True
            message.delivered_at = timezone.now()
            message.save()
        return Response({'status': 'delivered'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def mark_seen(self, request, pk=None):
        message = self.get_object()
        # Logic: Only mark as seen if the reader is NOT the sender
        if message.sender != request.user and not message.is_seen:
            message.is_seen = True
            message.seen_at = timezone.now()
            message.save()
        return Response({'status': 'read'}, status=status.HTTP_200_OK)