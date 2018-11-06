from django.conf.urls import url

from . import consumers
ASGI_APPLICATION = "mysite.routing.application"

websocket_urlpatterns = [
    url(r'^ws/nt', consumers.EchoConsumer),
]