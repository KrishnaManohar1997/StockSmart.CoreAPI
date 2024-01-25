from news.api import NewsAPIManager
from news.models import News


class NewsAPIService:
    news_api_manager = NewsAPIManager()
    ALLOWED_NEWSAPI_SOURCES = [
        "MoneyControl",
        "Livemint",
        "CNBCTV18",
        "Business Standard",
        "The Times of India",
        "BloombergQuint",
    ]
    ALLOWED_NEWS_KEYWORDS = ["NIFTY", "SENSEX"]

    def __is_article_allowed(self, title, description):
        # Handle case when description is None
        title_description = (
            title.split(" ") + description.split(" ") if description else ""
        )
        for keyword in self.ALLOWED_NEWS_KEYWORDS:
            if keyword in title_description:
                return True
        return False

    def get_stocksmart_news_json(self, news_article: dict):
        source_name = news_article.get("source", {}).get("name", None)
        news_title = news_article["title"]
        description = news_article["description"]
        if not source_name:
            return None
        if source_name in self.ALLOWED_NEWSAPI_SOURCES or self.__is_article_allowed(
            news_title, description
        ):
            return {
                "title": news_title,
                "description": description,
                "api_source": News.NewsAPISource.NEWS_API,
                "source_id": news_article["source"]["id"],
                "source_name": source_name,
                "url": news_article["url"],
                "image_url": news_article["urlToImage"],
                "published_at": news_article["publishedAt"],
            }

    def update_top_headlines(self):
        stocksmart_news = []
        for article in self.news_api_manager.get_top_headlines().get("articles", []):
            stocksmart_article_dict = self.get_stocksmart_news_json(article)
            if stocksmart_article_dict:
                stocksmart_news.append(stocksmart_article_dict)
        return stocksmart_news
