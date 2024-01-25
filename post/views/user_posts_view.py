from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated

from common.base_view import BaseView
from post.serializers import PostFeedSerializer
from post.services import ReactionService
from user.permissions import IsBlockedByUser
from user.services.user_service import UserService


class UserPostsView(BaseView):
    # Checks the target user_id using path, if blocked for requesting user
    permission_classes = [IsAuthenticated, IsBlockedByUser]
    post_serializer = PostFeedSerializer
    post_feed_paginator = LimitOffsetPagination()
    reaction_service = ReactionService()
    user_service = UserService()

    def get(self, request, social_user_id):
        target_user = self.user_service.get_user_by_id_or_none(social_user_id)
        if not target_user:
            return self.resource_not_found_response("User", social_user_id)

        user_created_posts = self.user_service.get_user_created_posts(target_user)
        post_feed = self.post_feed_paginator.paginate_queryset(
            user_created_posts, request
        )
        post_feed_data = self.post_serializer(post_feed, many=True).data
        posts_with_user_reaction_data = (
            self.reaction_service.merge_posts_with_user_reaction(
                post_feed_data, request.user.id
            )
        )
        return self.paginated_response(
            self.post_feed_paginator, "Posts", posts_with_user_reaction_data
        )
