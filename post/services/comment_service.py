from django.core.exceptions import ValidationError
from common.helper import DateTimeHelper

from common.helper.readable_serializer_error_translator import (
    translate_serializer_errors,
)
from notification.services import NotificationService
from post.models import Comment
from post.repositories import CommentRepository
from post.serializers import CreateCommentSerializer
from post.services import PostService
from user.services import UserFriendshipService


class CommentService:
    post_service = PostService()
    user_friendship_service = UserFriendshipService()
    comment_repo = CommentRepository()

    def __add_comment_to_post(self, user_id, post, comment_text):
        return self.comment_repo.add_comment_to_post(user_id, post, comment_text)

    def comment_on_post(self, comment_by_user_id, post_id, comment_text):
        post = self.post_service.get_post_by_id_or_none(post_id)
        if post is None:
            raise ValidationError("Post not found", code=404)
        self.user_friendship_service.is_requesting_user_blocked_by_user(
            requesting_user_id=comment_by_user_id,
            target_user_id=post.created_by_user_id,
            raise_error=True,
        )
        data = {
            "text": comment_text,
        }
        comment_serializer = CreateCommentSerializer(data=data)
        if not comment_serializer.is_valid():
            return False, translate_serializer_errors(comment_serializer.errors)
        comment = self.__add_comment_to_post(
            comment_by_user_id, post, comment_serializer.validated_data["text"]
        )
        self.post_service.update_comment_count(post, is_comment_added=True)
        POST_DELETE_MAX_DELAY = notification_delay = 300
        seconds_since_post_created = (
            DateTimeHelper.get_utc_datetime() - post.created_at
        ).seconds
        if seconds_since_post_created < POST_DELETE_MAX_DELAY:
            notification_delay = (
                POST_DELETE_MAX_DELAY - seconds_since_post_created + notification_delay
            )
        commented_by_user_id = str(comment_by_user_id)
        notify_user_id = str(post.created_by_user_id)
        if str(commented_by_user_id) != str(notify_user_id):
            NotificationService.send_comment_on_post_notification.apply_async(
                args=[notify_user_id, commented_by_user_id, str(comment.id)],
                countdown=notification_delay,  # 5-10 mins delay based on the Parent Post
            )
        return True, comment

    def get_comment_on_post_by_id_or_none(self, post_id, comment_id):
        try:
            return self.comment_repo.get_comment_on_post_by_id(post_id, comment_id)
        except Comment.DoesNotExist:
            return None

    def get_post_comments(self, post_id, requested_user_id):
        post = self.post_service.get_post_by_id_or_none(post_id)
        if post is None:
            raise ValidationError("Post not found", code=404)
        self.user_friendship_service.is_requesting_user_blocked_by_user(
            requesting_user_id=requested_user_id,
            target_user_id=post.created_by_user_id,
            raise_error=True,
        )
        if post.comment_count != 0:
            blocked_by_user_ids = self.user_friendship_service.get_blocked_by_user_ids(
                user_id=requested_user_id
            )
            return self.comment_repo.get_post_comments(post_id, blocked_by_user_ids)
        return None

    def update_comment_reaction_count(self, comment: Comment, is_reaction_added: bool):
        self.comment_repo.update_comment_reaction_count(comment, is_reaction_added)

    def delete_comment(self, comment) -> bool:
        return self.comment_repo.delete_comment(comment)

    def get_comment_by_id(self, comment_id):
        return self.comment_repo.get_comment_by_id(comment_id) or None
