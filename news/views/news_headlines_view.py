from common.helper.get_limited_paginated_results import get_limited_paginated_results
from rest_framework.pagination import LimitOffsetPagination

from common.base_view import PublicBaseView
from news.serializers import NewsSerializer
from news.services import NewsService


class NewsHeadlinesView(PublicBaseView):
    news_service = NewsService()
    news_serializer = NewsSerializer
    paginator = LimitOffsetPagination()

    def get(self, request):
        news_queryset = self.news_service.get_news_headlines()

        if request.user.is_authenticated:
            paginated_news_queryset = self.paginator.paginate_queryset(
                news_queryset, request
            )
        else:
            # Handles Non logged in user to restrict to max 10 news articles
            paginated_news_queryset = get_limited_paginated_results(
                request, news_queryset, self.paginator, 10
            )
        news_data = self.news_serializer(paginated_news_queryset, many=True).data
        return self.paginated_response(self.paginator, message="News", data=news_data)
