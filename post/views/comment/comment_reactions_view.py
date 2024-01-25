from common.base_view import BaseView
from post.services import ReactionService
from common.base_view import BaseView
from post.serializers import ContentReactionsSerializer
from post.services import ReactionService
from post.services import CommentService
from rest_framework.pagination import LimitOffsetPagination

from user.services.user_service import UserService


class CommentReactionsView(BaseView):
    reaction_service = ReactionService()
    comment_service = CommentService()
    paginator = LimitOffsetPagination()
    user_service = UserService()
    serializer = ContentReactionsSerializer

    def get(self, request, post_id, comment_id):
        comment = self.comment_service.get_comment_on_post_by_id_or_none(
            post_id, comment_id
        )
        if not comment:
            return self.resource_not_found_response(resource="Comment", id=comment_id)
        blocked_by_users = self.user_service.get_blocked_by_user_ids(request.user.id)
        reactions_qs = self.reaction_service.get_content_reactions(
            comment.id, blocked_by_users
        )
        paginated_set = self.paginator.paginate_queryset(reactions_qs, request)
        reacted_by_users = self.serializer(paginated_set, many=True).data
        data = [reaction["created_by_user"] for reaction in reacted_by_users]
        return self.paginated_response(self.paginator, "Likes", data=data)
