# chat/routing.py
from django.conf.urls import url
from django.urls import re_path, path

from . import consumers
from mapapp.consumers import MapGetConsumer, MapSendConsumer

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer),
    url(r'^ws/vcmsg/$', consumers.VcmsgConsumer),
    path('ws/map/', MapGetConsumer),
    path('ws/map_s/', MapSendConsumer),
]