from datetime import datetime, timezone

from news.helper.news_parser_helper import NewsParser
from news.models import News
from news.repositories import NewsRepository
from news.services.news_api_service import NewsAPIService
from smallcase.services.smallcase_service import SmallcaseService

from .google_news_service import GoogleNewsService


class NewsService:
    google_news_service = GoogleNewsService()
    news_repo = NewsRepository()
    news_api_service = NewsAPIService()
    smallcase_service = SmallcaseService()
    stocksmart_news_parser = NewsParser()
    # 3 Hours in Seconds
    NEWS_REFRESH_FREQUENCY = 10_800

    def __is_news_refresh_needed(self, last_fetched_at) -> bool:
        if not last_fetched_at:
            return True
        return (
            datetime.now(timezone.utc) - last_fetched_at
        ).total_seconds() >= self.NEWS_REFRESH_FREQUENCY

    def get_news_by_ticker(self, ticker):
        return self.news_repo.get_news_by_ticker(ticker)

    def process_latest_ticker_news(self, ticker):
        """Fetches Latest news from Google Rss source
        and invokes methods to store latest data

        Args:
            ticker (Stock): Stock instance
        """
        news_list, last_pub_date = self.google_news_service.get_ticker_news(ticker)
        self.update_ticker_news_records(ticker, news_list)
        ticker.latest_pub_news_date = last_pub_date
        ticker.last_news_fetched_at = datetime.now(tz=timezone.utc)
        ticker.save()

    def fetch_ticker_news(self, ticker):
        """Fetches Ticker news from DB
        If the last news fetched date is old
        fetches latest news and syncs with Db

        Args:
            ticker (Stock): Stock Instance for which news is to be fetched

        Returns:
            Queryset: News Queryset
        """
        if self.__is_news_refresh_needed(ticker.last_news_fetched_at):
            self.process_latest_ticker_news(ticker)
        return self.get_news_by_ticker(ticker)

    def update_tickers_on_news(self, news_queryset, ticker):
        return self.news_repo.update_tickers_on_news(news_queryset, ticker)

    def merge_ticker_news_by_title(self, ticker, news_titles):
        # Any News Articles that has same title
        # but tagged for Different Ticker will be merged
        news_queryset = self.news_repo.get_news_by_titles_excluded_by_ticker(
            ticker, news_titles
        )
        if news_queryset:
            self.update_tickers_on_news(news_queryset, ticker)

    def get_existing_news_titles_for_ticker(self, ticker, news_titles):
        return self.news_repo.get_existing_news_titles_for_ticker(
            ticker, news_titles
        ).values_list("title", flat=True)

    def get_existing_news_titles(self, news_titles):
        return self.news_repo.get_existing_news_titles(news_titles).values_list(
            "title", flat=True
        )

    def update_ticker_news_records(self, ticker, news_list):
        # Checks and Resolves Articles by Title
        # And Creates News Records
        news_titles = [news["title"] for news in news_list]
        self.merge_ticker_news_by_title(ticker, news_titles)
        exclude_news_titles = self.get_existing_news_titles_for_ticker(
            ticker, news_titles
        )
        news_object_list = []
        for news_dict in news_list:
            if (
                news_dict["title"] not in exclude_news_titles
                and len(news_dict["source_name"]) <= 64
            ):
                news_object_list.append(News(**news_dict))
        # Bulk Creates News Objects
        news_items = self.news_repo.bulk_create_news(
            news_object_list, ignore_conflicts=True
        )
        # Maps All News to the Ticker
        ticker.news_set.add(*news_items)

    def get_last_headlines_updated_time(self):
        return self.news_repo.get_last_headlines_updated_time()

    def process_new_headlines(self, headlines_list):
        news_titles = [news["title"] for news in headlines_list]
        exclude_news_titles = self.get_existing_news_titles(news_titles)
        news_object_list = []
        for news_dict in headlines_list:
            if news_dict["title"] not in exclude_news_titles:
                news_object_list.append(News(**news_dict))
        self.news_repo.bulk_create_news(news_object_list)

    def get_news_headlines(self):
        return self.news_repo.get_news_headlines()

    # Used under the Cron Job to Fetch and Update
    # Trending News
    def fetch_and_update_trending_news(self):
        headlines_list = self.news_api_service.update_top_headlines()
        self.process_new_headlines(headlines_list)

    def get_smallcase_news(self, smallcase):
        return self.news_repo.get_smallcase_news(smallcase)

    def fetch_smallcase_news(self, smallcase):
        if self.__is_news_refresh_needed(smallcase.last_news_fetched_at):
            self.process_smallcase_news(smallcase)

        return self.get_smallcase_news(smallcase)

    def process_smallcase_news(self, smallcase):
        """Fetches Latest news from Smallcase source
        and invokes methods to store latest data

        Args:
            smallcase (Smallcase): Instance of Smallcase
        """
        smallcase_news_list = self.smallcase_service.fetch_smallcase_news(smallcase)
        (
            news_titles,
            news_articles,
            last_pub_date,
        ) = self.stocksmart_news_parser.parse_news_dict(
            smallcase_news_list, News.NewsAPISource.SMALLCASE, smallcase
        )
        if not news_titles:
            return
        self.store_smallcase_news_articles(news_titles, news_articles, smallcase)
        smallcase.latest_pub_news_date = last_pub_date
        smallcase.last_news_fetched_at = datetime.now(tz=timezone.utc)
        smallcase.save()

    def update_smallcases_on_news(self, news_queryset, smallcase):
        self.news_repo.update_smallcases_on_news(news_queryset, smallcase)

    def store_smallcase_news_articles(
        self, news_titles: list, news_data: list, smallcase
    ):
        # Gets all News Articles that are not tagged for
        # the requesting smallcase, but do exist in DB
        news_queryset = self.news_repo.get_news_by_titles_excluded_by_smallcase(
            smallcase, news_titles
        )

        # Any News Articles that has same title
        # but tagged for Different Smallcase will be merged
        if news_queryset:
            self.update_smallcases_on_news(news_queryset, smallcase)

        # Since all the existing articles are tagged/Merged with
        # Requesting Smallcase, All those titles that match in DB
        # Can now be excluded
        exclude_news_titles = self.get_existing_news_titles(news_titles)
        news_object_list = []
        for news_dict in news_data:
            if news_dict["title"] not in exclude_news_titles:
                # List of Ticker Symbols
                news_dict.pop("tickers")
                news_object_list.append(News(**news_dict))
        news_items = self.news_repo.bulk_create_news(news_object_list)
        smallcase.news_set.add(*news_items)
