from datetime import datetime, timezone

from common.base_view import BaseView
from post.services import CommentService


class DeleteCommentView(BaseView):
    comment_service = CommentService()
    MAX_DELETE_COUNTDOWN = 5 * 60  # Minutes

    def is_comment_deleteable(self, comment):
        return (
            datetime.now(timezone.utc) - comment.created_at
        ).total_seconds() < self.MAX_DELETE_COUNTDOWN

    def post(self, request, post_id, comment_id):
        comment = self.comment_service.get_comment_on_post_by_id_or_none(
            post_id, comment_id
        )
        if not comment:
            return self.resource_not_found_response("Comment", id=comment_id)
        if request.user.id != comment.created_by_user_id:
            return self.resource_forbidden_response("Unauthorized to delete comment")
        if not self.is_comment_deleteable(comment):
            return self.bad_request_response("Cannot delete comment after 5 mins")
        is_comment_deleted = self.comment_service.delete_comment(comment)
        if not is_comment_deleted:
            return self.bad_request_response("Try again later to delete the comment")
        return self.resource_deleted_response(message="Ok", resource_id=comment_id)
