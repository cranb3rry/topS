# chat/routing.py
from django.conf.urls import url

from . import consumers
ASGI_APPLICATION = "mysite.routing.application"

websocket_urlpatterns = [
    url(r'^ws/chat/(?P<room_name>[^/]+)/$', consumers.ChatConsumer),
]