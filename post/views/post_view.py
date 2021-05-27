from common.helper.json_datetime_handler import datetime_handler
from common.helper.uuid_encoder import UUIDEncoder
from post.serializers import PostSerializer
from common.base_view import BaseView
from asgiref.sync import async_to_sync
from rest_framework.permissions import IsAuthenticated
import channels.layers
import json
from post.models import Post


class PostView(BaseView):
    channel_layer = channels.layers.get_channel_layer()
    permission_classes = [IsAuthenticated]

    def post(self, request):
        post_serializer = PostSerializer(data=request.data)
        if post_serializer.is_valid():
            print(post_serializer.validated_data)
            serialized_object = post_serializer.save()
            socket_data = serialized_object.__dict__
            post = Post.objects.get(id=socket_data.pop("id"))
            data = PostSerializer(post).data
            async_to_sync(self.channel_layer.group_send)(
                "chat_posts",
                {"type": "chat_message", "message": data},
            )
        else:
            return self.serializer_error_response(
                "Post Creation failed", post_serializer.errors
            )
        return self.data_response(
            message="Sent the Socket Events",
            data={"data": "Generated Socket Events"},
        )
