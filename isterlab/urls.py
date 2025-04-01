from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from chatbot.views import chatbot_view
from django.conf import settings
import django_eventstream
urlpatterns = [
    path('admin/', admin.site.urls),
    path("chatbot_view/", chatbot_view, name="chatbot_view"),
    path("",include("landing.urls")),
    path("events/", include(django_eventstream.urls), {"channels": ["test"]}),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

