import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Message, Conversation

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        # Ensure user is authenticated (Channels AuthMiddlewareStack handles this)
        if self.user.is_anonymous:
            await self.close()
            return

        self.room_name = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'chat_{self.room_name}'

        # Security check: Is this user a participant in the conversation?
        if await self.is_participant(self.room_name):
            await self.channel_layer.group_add(self.room_group_name, self.channel_name)
            await self.accept()
        else:
            await self.close()

    async def receive(self, text_data):
        """
        Handles incoming data from Flutter. 
        It could be a new 'message' or a 'receipt_update'.
        """
        data = json.loads(text_data)
        data_type = data.get('type', 'message') # Default to message

        if data_type == 'message':
            message_text = data['message']
            # Save to database
            saved_msg = await self.save_message(self.room_name, message_text)

            # Broadcast message to the group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message_id': saved_msg.id,
                    'message': message_text,
                    'sender': self.user.email,
                    'created_at': str(saved_msg.created_at)
                }
            )
        
        elif data_type == 'receipt_update':
            # When Flutter confirms it saved the msg locally
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'message_receipt',
                    'message_id': data['message_id'],
                    'status': data['status']
                }
            )

    async def chat_message(self, event):
        """Handler for 'chat_message' type events"""
        await self.send(text_data=json.dumps(event))

    async def message_receipt(self, event):
        """
        FIXED INDENTATION: 
        Handler for 'message_receipt' type events (receipt_update)
        """
        await self.send(text_data=json.dumps({
            'type': 'receipt_update',
            'message_id': event['message_id'],
            'status': event['status']
        }))

    @database_sync_to_async
    def is_participant(self, convo_id):
        return Conversation.objects.filter(id=convo_id, participants=self.user).exists()

    @database_sync_to_async
    def save_message(self, convo_id, text):
        convo = Conversation.objects.get(id=convo_id)
        return Message.objects.create(
            conversation=convo, 
            sender=self.user, 
            text=text
        )