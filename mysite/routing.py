from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import chat.routing
from notifier.consumers import EchoConsumer
from chat.consumers import ChatConsumer
from django.conf.urls import url

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': AuthMiddlewareStack(
        URLRouter(
            #chat.routing.websocket_urlpatterns,
            [url(r'^ws/nt/', EchoConsumer),
             url(r'^ws/chat/(?P<room_name>[^/]+)/$', ChatConsumer),
             ]
        )
    ),
})