from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ConversationViewSet, MessageViewSet, ChatThreadListView

router = DefaultRouter()
# 1. Register messages for your receipt actions (acknowledge_receipt, mark_seen)
router.register(r'messages', MessageViewSet, basename='messages')

# 2. Use the router for conversations ONLY if you need ViewSet actions for specific threads
# e.g., /api/chat/conversations/1/
router.register(r'conversations', ConversationViewSet, basename='conversations')

urlpatterns = [
    # This handles /api/chat/threads/ manually for your custom List View
    path('threads/', ChatThreadListView.as_view(), name='chat-threads'),
    
    # This includes the rest (messages, conversations)
    path('', include(router.urls)),
]