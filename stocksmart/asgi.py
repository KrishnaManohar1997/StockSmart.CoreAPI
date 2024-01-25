"""
ASGI config for stocksmart project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "stocksmart.settings")
os.environ.setdefault("ASGI_THREADS", "3")
# Pre-Initialization before importing App related Modules
# Helps avoid Circular Imports
django_asgi_app = get_asgi_application()

import stocksmart.routing
from stocksmart.socket_auth_middleware import SocketTokenAuthMiddleware


application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AllowedHostsOriginValidator(
            SocketTokenAuthMiddleware(
                URLRouter(stocksmart.routing.websocket_urlpatterns)
            )
        ),
    }
)
