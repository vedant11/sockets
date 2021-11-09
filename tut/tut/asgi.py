"""
ASGI config for tut project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

# core
import os

# django
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
from django.urls import re_path

# local
import core.wsconsumer as cons


urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', cons.ChatConsumer.as_asgi()),
]


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tut.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            urlpatterns
        )
    ),
})
