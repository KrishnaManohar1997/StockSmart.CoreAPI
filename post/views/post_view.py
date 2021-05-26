from common.base_view import BaseView
from asgiref.sync import async_to_sync

import channels.layers


class PostView(BaseView):
    channel_layer = channels.layers.get_channel_layer()

    def get(self, request):
        import random

        async_to_sync(self.channel_layer.group_send)(
            "chat_posts",
            {"type": "chat_message", "message": f"connected {random.randint(10,15)}"},
        )
        return self.data_response(
            message="Sent the Socket Events",
            data={"data": "Generated Socket Events"},
        )
