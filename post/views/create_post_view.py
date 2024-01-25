from common.base_view import BaseView
from post.serializers import PostFeedSerializer
from post.services import PostService
from notification.services import NotificationService


class CreatePostView(BaseView):
    post_service = PostService()
    post_serializer = PostFeedSerializer

    def post(self, request):
        is_valid, serializer = self.post_service.create_post_from_request(request)
        if not is_valid:
            return self.serializer_error_response(
                message="Creating post failed", serializer_errors=serializer.errors
            )
        NotificationService.send_post_created_notification.apply_async(
            args=[serializer.id], countdown=301  # 5 Minutes delay
        )
        return self.resource_created_data_response(
            resource="Post",
            resource_id=serializer.id,
            data=self.post_serializer(serializer).data,
        )
