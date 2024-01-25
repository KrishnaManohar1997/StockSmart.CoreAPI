import structlog
from django.db import transaction
from django.db.models import F

from post.models import Comment
from post.repositories import PostRepository

logger = structlog.getLogger("django.server")


class CommentRepository:
    def get_post_comments(self, post_id: str, blocked_by_user_ids: list):
        return (
            Comment.objects.filter(object_id=post_id)
            .exclude(created_by_user_id__in=blocked_by_user_ids)
            .order_by("-created_at")
            .prefetch_related("created_by_user")
        )

    def add_comment_to_post(self, user_id, post, comment_text):
        return Comment.objects.create(
            created_by_user_id=user_id, content_object=post, text=comment_text
        )

    def get_comment_on_post_by_id(self, post_id, comment_id):
        return Comment.objects.get(id=comment_id, object_id=post_id)

    def update_comment_reaction_count(self, comment: Comment, is_reaction_added: bool):
        if is_reaction_added:
            comment.reaction_count = F("reaction_count") + 1
        else:
            comment.reaction_count = F("reaction_count") - 1

        comment.save(update_fields=["reaction_count"])

    @transaction.atomic
    def delete_comment(self, comment):
        try:
            with transaction.atomic():
                PostRepository().update_comment_count(
                    comment.content_object, is_comment_added=False
                )
                comment.reactions.all().delete()
                comment.delete()
                return True
        except Exception as error:
            logger.error(f"Failed deleting comment {comment.id} {error}")
        return False

    def get_comment_by_id(self, comment_id):
        return Comment.objects.filter(id=comment_id).first()
