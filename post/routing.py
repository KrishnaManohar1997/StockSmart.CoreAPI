from django.urls import re_path

from .consumers import post_create_consumer

websocket_urlpatterns = [
    re_path(r"ws/posts/", post_create_consumer.PostCreationConsumer.as_asgi()),
]
