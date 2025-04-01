import django
import os
from django.core.asgi import get_asgi_application
from channels.security.websocket import OriginValidator
from chatbot.routing import websocket_urlpatterns

django_asgi_app = get_asgi_application()

print("start channels")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'isterlab.settings')
django.setup()
# Initialize Django ASGI application early to ensure the AppRegistry
# is populated before importing code that may import ORM models.
from channels.routing import ProtocolTypeRouter,URLRouter

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    'websocket': OriginValidator( 
    URLRouter(
    websocket_urlpatterns
    ),
    ["*"]),
    }) 