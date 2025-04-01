from django.shortcuts import render
from django_eventstream import send_event

# Create your views here.

def chatbot_view(request):
    send_event("test", "message", {"text": "hello world"})
    return render(request, 'chatbot/home.html')