"""
ASGI config for easyline project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'easyline.settings')
django.setup()

# 
from channels.routing import ProtocolTypeRouter, URLRouter, ChannelNameRouter

from api_async import routing
from api_async.middlewares.AuthMiddleware import TokenAuthMiddleware

application = get_asgi_application()

application = ProtocolTypeRouter({
    # "http": get_asgi_application(),
     "channel": ChannelNameRouter(
        routing.channels_urlspattern
    ),
    "websocket": TokenAuthMiddleware(
        URLRouter(
            routing.urlpatterns
        )
    )
})

