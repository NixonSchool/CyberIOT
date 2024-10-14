import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        user_ids = self.room_name.split('_')
        self.room_group_name = f'chat_{min(user_ids)}_{max(user_ids)}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender_id = text_data_json['sender_id']
        recipient_id = text_data_json['recipient_id']

        await self.save_message(sender_id, recipient_id, message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender_id': sender_id
            }
        )

    async def chat_message(self, event):
        message = event['message']
        sender_id = event['sender_id']

        await self.send(text_data=json.dumps({
            'message': message,
            'sender_id': sender_id,
            'timestamp': await self.get_timestamp()
        }))

    @database_sync_to_async
    def save_message(self, sender_id, recipient_id, content):
        from .models import Message  # Import here to avoid AppRegistryNotReady error
        User = get_user_model()
        sender = User.objects.get(id=sender_id)
        recipient = User.objects.get(id=recipient_id)
        return Message.objects.create(sender=sender, recipient=recipient, content=content)

    @database_sync_to_async
    def get_timestamp(self):
        from django.utils import timezone
        return timezone.now().strftime('%H:%M')
