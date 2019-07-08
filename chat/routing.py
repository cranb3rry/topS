# chat/routing.py
from django.conf.urls import url
from django.urls import path


from . import consumers
from mapapp.consumers import MapGetConsumer, MapSendConsumer

websocket_urlpatterns = [
    url(r'^ws/chat/(?P<room_name>[^/]+)/$', consumers.ChatConsumer),
    url(r'^ws/vcmsg/$', consumers.VcmsgConsumer),
    path('ws/map/', MapGetConsumer),
    path('ws/map_s/', MapSendConsumer),
]