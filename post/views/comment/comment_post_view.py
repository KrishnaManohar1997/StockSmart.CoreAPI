from common.base_view import BaseView
from post.serializers import CommentsViewSerializer
from post.services import CommentService, ReactionService


class CommentPostView(BaseView):
    comment_service = CommentService()
    reaction_service = ReactionService()
    comment_serializer = CommentsViewSerializer

    def post(self, request, post_id):
        comment_text = request.data.get("text")
        if not comment_text:
            return self.bad_request_response("Invalid request")
        is_commented, message = self.comment_service.comment_on_post(
            request.user.id, post_id, comment_text
        )
        if not is_commented:
            return self.bad_request_response(message=message)
        comment = message
        return self.resource_created_data_response(
            resource="Comment",
            resource_id=comment.id,
            data=self.comment_serializer(comment).data,
        )
