from django.urls import re_path

from .consumers import notification_consumer

websocket_urlpatterns = [
    re_path(r"ws/notifications/", notification_consumer.NotificationConsumer.as_asgi()),
]
