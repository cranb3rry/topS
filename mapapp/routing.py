# chat/routing.py
from django.conf.urls import url

from . import consumers

websocket_urlpatterns = [
    url(r'^ws/map/$', consumers.MapGetConsumer),
    url(r'^ws/map_s/$', consumers.MapSendConsumer),
    
]