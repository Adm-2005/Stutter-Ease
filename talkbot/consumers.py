import json
import wit
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import ChatMessage


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = "general"
        self.room_group_name = f"chat_{self.room_name}"

        async_to_sync(self.channel_layer.group_add)(self.room_group_name,
                                                    self.channel_name)

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(self.room_group_name,
                                                        self.channel_name)

    def process_message_with_wit(self, message):
        wit_access_token = 'KSXTZXMADTRDMFPB2UKGBZPDZAYGO6FS'
        client = wit.Wit(access_token = wit_access_token)
      
        response = client.message(message)
        intent = response['intents'][0]['name'] if response.get('intents') else 'Unknown'

        return intent
  
    def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        sender = data['sender']

        #processing message using wit.ai
        intent = self.process_message_with_wit(message)
        
        #saving message to database
        ChatMessage.objects.create(sender=sender, message=message)

        async_to_sync(self.channel_layer.group_send)(self.room_group_name, {
            'type': 'chat.message',
            'sender': sender,
            'message': intent,
        })

    def chat_message(self, event):
        #Sends message to WebSocket
        message = event['message']
        sender = event['sender']
        self.send(text_data=json.dumps({'sender': sender, 'message': message}))
