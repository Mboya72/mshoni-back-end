from rest_framework import serializers
from .models import Conversation, Message
from users.serializers import UserSerializer # Assuming you have one

class MessageSerializer(serializers.ModelSerializer):
    sender_email = serializers.ReadOnlyField(source='sender.email')
    
    class Meta:
        model = Message
        fields = ['id', 'conversation', 'sender', 'sender_email', 'text', 'image', 'is_read', 'created_at']

class ConversationSerializer(serializers.ModelSerializer):
    last_message = serializers.SerializerMethodField()
    participants_details = UserSerializer(source='participants', many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ['id', 'participants', 'participants_details', 'last_message', 'updated_at']

    def get_last_message(self, obj):
        last = obj.messages.last()
        if last:
            return MessageSerializer(last).data
        return None