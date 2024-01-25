from rest_framework.pagination import LimitOffsetPagination

from common.base_view import BaseView
from post.serializers import PostFeedSerializer
from post.services import PostService, ReactionService


class ExplorePostView(BaseView):
    post_serializer = PostFeedSerializer
    post_feed_paginator = LimitOffsetPagination()
    reaction_service = ReactionService()
    post_service = PostService()

    def get(self, request):
        posts_queryset = self.post_service.get_posts_by_filter(request)
        paginated_posts_queryset = self.post_feed_paginator.paginate_queryset(
            posts_queryset, request
        )
        post_feed_data = self.post_serializer(paginated_posts_queryset, many=True).data
        posts_with_user_reaction_data = (
            self.reaction_service.merge_posts_with_user_reaction(
                post_feed_data, request.user.id
            )
        )
        return self.paginated_response(
            self.post_feed_paginator, "Posts", posts_with_user_reaction_data
        )
