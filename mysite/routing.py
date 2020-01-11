from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter, ChannelNameRouter
from chat.routing import websocket_urlpatterns 
from chat.consumers import ChatConsumer, TaskConsumer, TwitchChatConsumer, OkChatConsumer, QwDntConsumer
from django.conf.urls import url

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),

    "channel": ChannelNameRouter({
        "qw": QwDntConsumer,
        "tasks": TaskConsumer,
        "tw": TwitchChatConsumer,
        "ok": OkChatConsumer}),


})
