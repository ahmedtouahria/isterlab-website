import json
import re
import uuid
from datetime import datetime
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from openai import OpenAI
from decouple import config
class ChatConsumer(WebsocketConsumer):
    """
    AI-powered Chatbot Consumer for handling WebSocket connections.
    - Connects to a chat room.
    - Receives user messages.
    - Generates AI-based chatbot responses.
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.room_name = None
        self.room_group_name = None
        self.client = OpenAI(api_key=config("OPENAI_API_KEY"))
    
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
        
        bot_response = self.generate_ai_response(user_message)
        
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
        """Allow only alphanumeric characters and basic punctuation."""
        return bool(re.match(r'^[a-zA-Z0-9\s!?.,]*$', message))
    
    def generate_ai_response(self, user_message):
        """Generates a response using DeepSeek AI."""
        try:
            response = self.client.chat.completions.create(
                model="o3-mini",
                messages=[
                    {"role": "system", "content": """
                     You are a helpful assistant providing information about the isterlab-global.com website.
                     please the answer must be less than 100 words.
                     
                     """},
                    {"role": "user", "content": user_message},
                ],
                stream=False
            )
            print (response)
            return response.choices[0].message.content
        except Exception as e:
            print(e)
            return "I'm having trouble generating a response. Please try again later."
    
    def send_error_message(self, error_message):
        self.send(text_data=json.dumps({
            'error': error_message
        }))
