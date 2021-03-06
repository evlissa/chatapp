# chat/consumers.py
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from datetime import datetime
from .models import ChatMessage, Account
import json


class ChatConsumer(WebsocketConsumer):

    # загрузка истории сообщений
    def fetch_messages(self, data):
        messages = ChatMessage.last_15_messages()
        content = {
            'command':'messages',
            'messages': self.messages_to_json(messages)
        }
        self.send_message(content)

    # создание нового сообщения
    def new_message(self, data):
        authorname = self.scope["user"].username
        author = Account.objects.get(username = authorname)
        message = ChatMessage.objects.create(
            author =  author,
            content = data['message'],
            timestamp = datetime.now(),
            visualdate = datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        content = {
            'command':'new_message',
            'message': self.message_to_json(message)
        }
        return self.send_chat_message(content)

    def messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result

    def message_to_json(self, message):
        return{
            'author': message.author.username,
            'content': message.content,
            'timestamp': str(message.timestamp),
            'visualdate': message.visualdate,
        }

    commands = {
        'fetch_messages': fetch_messages,
        'new_message': new_message
    }

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Зайти в  room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Выйти из room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
        
    # Получить сообщение из вебсокета
    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data['command']](self, data)

    def send_chat_message(self, message):
        # Отправить сообщение в room group
        async_to_sync(self.channel_layer.group_send)( 
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    def send_message(self, message):
        self.send(text_data=json.dumps(message))

    def chat_message(self, event):
        message = event['message']
        self.send(text_data=json.dumps(message))

