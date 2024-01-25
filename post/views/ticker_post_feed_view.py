from user.services.user_friendship_service import UserFriendshipService
from ticker.services.ticker_service import TickerService
from rest_framework.pagination import LimitOffsetPagination

from common.base_view import PublicBaseView
from common.helper.get_limited_paginated_results import get_limited_paginated_results
from post.services import ReactionService

from post.serializers import PostFeedSerializer


class TickerPostFeedView(PublicBaseView):
    post_serializer = PostFeedSerializer
    post_feed_paginator = LimitOffsetPagination()
    reaction_service = ReactionService()
    ticker_service = TickerService()
    user_friendship_service = UserFriendshipService()

    def get(self, request, ticker_id: str):
        ticker_type = request.query_params.get("tickerType", "Stock")
        ticker = self.ticker_service.get_ticker_by_id(ticker_id, ticker_type)
        blocked_by_user_ids = self.user_friendship_service.get_blocked_by_user_ids(
            request.user.id
        )
        stock_mentioned_posts_queryset = self.ticker_service.get_ticker_mentioned_posts(
            ticker, blocked_by_user_ids
        )
        if request.user.is_authenticated:
            paginated_posts_queryset = self.post_feed_paginator.paginate_queryset(
                stock_mentioned_posts_queryset, request
            )
        else:
            # Handles Non logged in user to restrict to max 10 posts
            paginated_posts_queryset = get_limited_paginated_results(
                request, stock_mentioned_posts_queryset, self.post_feed_paginator, 10
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
