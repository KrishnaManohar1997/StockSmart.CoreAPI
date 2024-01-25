from common.base_view import BaseView
from post.serializers import ContentReactionsSerializer
from post.services import ReactionService
from post.services import PostService
from rest_framework.pagination import LimitOffsetPagination

from user.services.user_service import UserService


class PostReactionsView(BaseView):
    reaction_service = ReactionService()
    post_service = PostService()
    paginator = LimitOffsetPagination()
    user_service = UserService()
    serializer = ContentReactionsSerializer

    def get(self, request, post_id):
        post = self.post_service.get_post_by_id_or_none(post_id)
        if not post:
            return self.resource_not_found_response(resource="Post", id=post_id)
        blocked_by_users = self.user_service.get_blocked_by_user_ids(request.user.id)
        reactions_qs = self.reaction_service.get_content_reactions(
            post.id, blocked_by_users
        )
        paginated_set = self.paginator.paginate_queryset(reactions_qs, request)
        reacted_by_users = self.serializer(paginated_set, many=True).data
        data = [reaction["created_by_user"] for reaction in reacted_by_users]
        return self.paginated_response(self.paginator, "Likes", data=data)
