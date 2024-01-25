from news.models import News


class NewsRepository:
    def get_news_by_ticker(self, ticker):
        return ticker.news_set.all().order_by("-published_at")

    def bulk_create_news(self, news_object_list: list, ignore_conflicts=False):
        return News.objects.bulk_create(
            news_object_list, ignore_conflicts=ignore_conflicts
        )

    def get_existing_news_titles_for_ticker(self, ticker, news_titles):
        return ticker.news_set.filter(title__in=news_titles)

    def get_existing_news_titles(self, news_titles):
        return News.objects.filter(title__in=news_titles)

    def get_news_by_titles_excluded_by_ticker(self, ticker, news_titles):
        return News.objects.filter(title__in=news_titles).exclude(tickers=ticker)

    def get_news_by_titles_excluded_by_smallcase(self, smallcase, news_titles):
        return News.objects.filter(title__in=news_titles).exclude(smallcases=smallcase)

    def update_tickers_on_news(self, news_queryset, ticker):
        return ticker.news_set.add(*news_queryset)

    def update_smallcases_on_news(self, news_queryset, smallcase):
        return smallcase.news_set.add(*news_queryset)

    def get_last_headlines_updated_time(self):
        return getattr(
            News.objects.filter(api_source=News.NewsAPISource.NEWS_API)
            .order_by("-created_at")
            .first(),
            "created_at",
            None,
        )

    def get_news_headlines(self):
        return News.objects.filter(api_source=News.NewsAPISource.NEWS_API).order_by(
            "-published_at"
        )

    def get_smallcase_news(self, smallcase):
        return smallcase.news_set.filter(
            api_source=News.NewsAPISource.SMALLCASE
        ).order_by("-published_at")
