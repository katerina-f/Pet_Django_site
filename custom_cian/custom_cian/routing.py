from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path

from main.consumers import ChatConsumer


application = ProtocolTypeRouter({
    "websocket": AuthMiddlewareStack(
        URLRouter([
            path("chat/", ChatConsumer.as_asgi()),
        ]),
    ),
})
