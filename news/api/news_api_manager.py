from django.conf import settings
from newsapi import NewsApiClient


class NewsAPIManager:
    # https://newsapi.org/docs
    __instance = None

    @staticmethod
    def get_news_client():
        if NewsAPIManager.__instance is None:
            NewsAPIManager()
        return NewsAPIManager.__instance

    def __init__(self):
        if NewsAPIManager.__instance is not None:
            # This ensures that instance is already available
            pass
        else:
            NewsAPIManager.__instance = NewsApiClient(api_key=settings.NEWS_API_KEY)

    def get_top_headlines(self):
        return self.get_news_client().get_top_headlines(
            category="business", language="en", country="in", page_size=40
        )
