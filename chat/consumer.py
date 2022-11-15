from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Chat , Room 
from django.contrib.auth.models import User 

import json, html
    
class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):

        self.room_code = self.scope["url_route"]["kwargs"]["room_code"]
        self.group_room_code = f'chat_{self.room_code}'
        self.sender = str(self.scope.get("user"))

        self.room_model = await self.get_room_model()
        
        if self.sender != "AnonymousUser":
            self.user = await self.get_user()
        else:
            self.user = None
        
        await self.channel_layer.group_add(self.group_room_code, self.channel_name)
        
        await self.channel_layer.group_send(
            self.group_room_code, 
            {
                "type":"chat_message",
                "message":"Joined the room!",
                "sender":self.sender
            }
        )
        
        await self.accept()
    
    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.group_room_code, self.channel_name)
    
    async def receive(self, text_data=None, bytes_data=None):
        
        json_data = json.loads(text_data)
        message = json_data.get('message')

        await self.save_message(message)

        
        await self.channel_layer.group_send(
            self.group_room_code, 
            {
                "type":"chat.message",
                "message":message,
                "sender":self.sender
            }
        )
    async def chat_message(self, text_data):
        message = html.escape(text_data.get("message"))
        sender = text_data.get('sender')

        await self.send(text_data=json.dumps({"message":message,"sender":sender}))

    @database_sync_to_async
    def save_message(self, text: str):
        if self.user:
            chat = Chat.objects.create(
                from_user=self.user,
                text=text
            )
            
            self.room_model.chat_set.add(chat)

            return chat
    
    @database_sync_to_async 
    def get_room_model(self):
        return Room.objects.get(room_code=self.room_code)

    @database_sync_to_async
    def get_user(self):
        return User.objects.get(username=self.sender)

class NotifConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add('notif_chat', self.channel_name)
    
        await self.accept()
    
    async def receive(self, text_data=None, bytes_data=None):
        json_text = json.loads(text_data)
        
        await self.channel_layer.group_send(
            'notif_chat',
            {
                'type':'send.notif',
                'room':json_text.get('room')
            }
        )
    
    async def send_notif(self, text_data):

        await self.send(text_data=json.dumps(text_data))