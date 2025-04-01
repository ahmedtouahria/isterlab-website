import json
import re
import uuid
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from datetime import datetime


import json
import re
from datetime import datetime
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

class ChatConsumer(WebsocketConsumer):
    """
    Chatbot Consumer for handling WebSocket connections.
    - Connects to a chat room.
    - Receives user messages.
    - Sends automated chatbot responses.
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.room_name = None
        self.room_group_name = None
    
    def connect(self):
        self.room_name = str(uuid.uuid4())  # Generate a random room name
        self.room_group_name = f'chat_{self.room_name}'
        
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name,
        )
        
        self.accept()
    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        user_message = text_data_json.get("message", "")
        print("Received:", user_message)
        
        if not self.is_valid_message(user_message):
            self.send_error_message("Invalid message format.")
            return
        
        bot_response = self.generate_bot_response(user_message)
        
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': "chat.message",
                'message': bot_response,
                'timestamp': f"{datetime.now()}"
            }
        )
    
    def chat_message(self, event):
        self.send(text_data=json.dumps(event))

    def is_valid_message(self, message):
        """Allow only alphanumeric characters and spaces."""
        return bool(re.match(r'^[a-zA-Z0-9\s!?.,]*$', message))
    
    def generate_bot_response(self, user_message):
        """Basic chatbot logic to respond to messages."""
        user_message = user_message.lower()
        if "hello" in user_message:
            return "Hello! How can I help you today?"
        elif "how are you" in user_message:
            return "I'm just a bot, but I'm doing great! How about you?"
        elif "bye" in user_message:
            return "Goodbye! Have a great day!"
        else:
            return "I'm not sure how to respond to that. Can you ask something else?"
    
    def send_error_message(self, error_message):
        self.send(text_data=json.dumps({
            'error': error_message
        }))