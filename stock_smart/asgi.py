"""
ASGI config for stock_smart project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os
from stock_smart.socket_auth_middleware import QueryAuthMiddleware
import post.routing

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "stock_smart.settings")

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": QueryAuthMiddleware(URLRouter(post.routing.websocket_urlpatterns)),
    }
)
