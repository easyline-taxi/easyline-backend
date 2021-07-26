"""
ASGI config for easyline project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
# 
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.conf.urls import url
from .channelsMiddleware import TokenAuthMiddleware
from api.channels.websocket import ChatConsumer
# 

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'easyline.settings')

# application = get_asgi_application()

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": TokenAuthMiddleware(
        URLRouter([
            # url(r"^chat/admin/$", AdminChatConsumer.as_asgi()),
            url(r"^chat/$", ChatConsumer.as_asgi()),
        ])
    )
    # Just HTTP for now. (We can add other protocols later.)
})

