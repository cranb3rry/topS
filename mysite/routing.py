from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter, ChannelNameRouter
from chat.routing import websocket_urlpatterns 
from chat.consumers import ChattyBotConsumer
from django.conf.urls import url

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns,
            # [url(r'^ws/nt/', EchoConsumer),
            #  #url(r'^ws/chat/(?P<room_name>[^/]+)/$', ChatConsumer),
            #  ]
        ),
    ),

    "tm": ChattyBotConsumer,

    "channel": ChannelNameRouter({
        "irc-1": ChattyBotConsumer,}),

})
