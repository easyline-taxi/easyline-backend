"""
ASGI config for easyline project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
import django

# 
from channels.routing import ProtocolTypeRouter, URLRouter, ChannelNameRouter
from django.conf.urls import url
from task.routing import channels_urlspattern

# # 

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'easyline.settings')
django.setup()
from websocket.middlewares.channelsMiddleware import TokenAuthMiddleware
import websocket.routing


# application = get_asgi_application()

application = ProtocolTypeRouter({
    # "http": get_asgi_application(),
     "channel": ChannelNameRouter(
        channels_urlspattern
    ),
    "websocket": TokenAuthMiddleware(
        URLRouter(
            websocket.routing.url_patterns
        )
    )
})

