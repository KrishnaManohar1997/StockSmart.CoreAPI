from datetime import datetime, timezone

import structlog

from common.base_view import BaseView
from post.services import PostService

logger = structlog.getLogger("django.server")


class DeletePostView(BaseView):
    post_service = PostService()
    MAX_DELETE_COUNTDOWN = 5 * 60  # Minutes

    def is_post_deleteable(self, post):
        return (
            datetime.now(timezone.utc) - post.created_at
        ).total_seconds() < self.MAX_DELETE_COUNTDOWN

    def post(self, request, post_id):
        post = self.post_service.get_post_by_id_or_none(post_id)

        if not post:
            return self.resource_not_found_response("Post", id=post_id)

        if post.created_by_user_id != request.user.id:
            return self.resource_forbidden_response(
                "Cannot perform the requested action"
            )

        if not self.is_post_deleteable(post):
            return self.bad_request_response("Cannot delete post after 5 Minutes")

        is_post_deleted = self.post_service.delete_post(post)
        if not is_post_deleted:
            return self.bad_request_response("Please try again later")
        return self.resource_deleted_response("Post", post_id)
