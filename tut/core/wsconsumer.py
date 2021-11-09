# native
import json
from asgiref.sync import async_to_sync

# django
from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_' + self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        # connection will be rejected and closed
        # if not for the following:
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from Client through WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send event with type: message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # chat message event
    async def chat_message(self, event):
        message = event['message']

        # Send message to Client through WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))

    async def incoming_flood(self, event):
        message = event['value']

        await self.send(text_data=json.dumps({
            'message': message
        }))


class SyncChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_' + self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        # connection will be rejected and closed
        # if not for the following:
        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from Client through WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send event with type: message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # chat message event
    def chat_message(self, event):
        message = event['message']

        # Send message to Client through WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))

    def incoming_flood(self, event):
        message = event['value']

        self.send(text_data=json.dumps({
            'message': message
        }))
