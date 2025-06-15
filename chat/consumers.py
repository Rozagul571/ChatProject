# chat/consumers.py
import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from .models import Room, Message

# Logger sozlash
logger = logging.getLogger(__name__)


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        print(f"🔗 WebSocket CONNECT: Room={self.room_name}, Group={self.room_group_name}")

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
        print(f"✅ WebSocket ACCEPTED: {self.room_name}")

        # Get or create room
        room = await self.get_or_create_room()
        print(f"🏠 Room created/found: {room}")

    async def disconnect(self, close_code):
        print(f"❌ WebSocket DISCONNECT: Room={self.room_name}, Code={close_code}")
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        print(f"📨 WebSocket RECEIVE: {text_data}")

        try:
            text_data_json = json.loads(text_data)
            message = text_data_json['message']
            username = text_data_json['username']

            print(f"👤 User: {username}")
            print(f"💬 Message: {message}")
            print(f"🏠 Room: {self.room_name}")

            # Save message to database
            saved_message = await self.save_message(username, message)
            print(f"💾 Message saved to DB: {saved_message}")

            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'username': username,
                    'timestamp': str(await self.get_current_time())
                }
            )
            print(f"📤 Message sent to group: {self.room_group_name}")

        except Exception as e:
            print(f"❌ ERROR in receive: {e}")
            import traceback
            traceback.print_exc()

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        timestamp = event['timestamp']

        print(f"📥 Sending to WebSocket: {username}: {message}")

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'timestamp': timestamp
        }))
        print(f"✅ Message sent to client")

    @database_sync_to_async
    def get_or_create_room(self):
        try:
            room, created = Room.objects.get_or_create(name=self.room_name)
            print(f"🏠 Room {'created' if created else 'found'}: {room.name}")
            return room
        except Exception as e:
            print(f"❌ ERROR creating room: {e}")
            return None

    @database_sync_to_async
    def save_message(self, username, message):
        try:
            user, created = User.objects.get_or_create(username=username)
            print(f"👤 User {'created' if created else 'found'}: {user.username}")

            room = Room.objects.get(name=self.room_name)
            message_obj = Message.objects.create(
                room=room,
                user=user,
                content=message
            )
            print(f"💾 Message saved: ID={message_obj.id}")
            return message_obj
        except Exception as e:
            print(f"❌ ERROR saving message: {e}")
            import traceback
            traceback.print_exc()
            return None

    @database_sync_to_async
    def get_current_time(self):
        from django.utils import timezone
        return timezone.now()