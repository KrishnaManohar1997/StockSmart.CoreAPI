from datetime import datetime, timedelta, timezone

import requests
import xmltodict
from django.core.exceptions import ValidationError

from news.models import News
import structlog

logger = structlog.getLogger("django.server")


class GoogleNewsRssManager:
    GOOGLE_RSS_SEARCH = "https://news.google.com/rss/search"

    def get_ticker_news(self, ticker):
        response = self.get_ticker_news_rss(ticker)
        return self.parse_google_rss_stock_response(ticker, response)

    def get_ticker_news_rss(self, ticker):
        response = requests.get(
            f"{self.GOOGLE_RSS_SEARCH}?hl=en-IN&gl=IN&ceid=IN:en",
            params={"q": ticker.symbol},
        )
        if response.status_code != 200:
            raise ValidationError("Google Rss Feed Response is invalid", code=400)
        return response

    def parse_google_rss_stock_response(self, ticker, response):
        news_dict = xmltodict.parse(response.content)
        news_list = []
        if "item" in news_dict["rss"]["channel"]:
            try:
                news_api_source = News.NewsAPISource.GOOGLE_RSS
                latest_pub_date = datetime.now(timezone.utc) - timedelta(days=50)
                news_items = news_dict["rss"]["channel"]["item"]
                # When a Single News Item is present
                # Instead of List it would be a dict
                if isinstance(news_items, dict):
                    news_items = [news_items]
                for news_item in news_items:
                    # Date format Tue, 07 Sep 2021 09:31:24 GMT
                    published_at = datetime.strptime(
                        news_item["pubDate"], "%a, %d %b %Y %H:%M:%S GMT"
                    ).replace(tzinfo=timezone.utc)
                    # Makes Sure that new news will be fetched
                    if (
                        # If doesn't have a latest published article date (None)
                        not ticker.latest_pub_news_date
                        or
                        # Check all articles are after the latest date
                        ticker.latest_pub_news_date < published_at
                    ):
                        news_list.append(
                            {
                                "published_at": published_at,
                                "title": news_item["title"],
                                "url": news_item["link"],
                                "image_url": None,
                                "source_name": news_item["source"]["#text"],
                                "api_source": news_api_source,
                            }
                        )
                        # Stores the most recent Published Date
                        if published_at > latest_pub_date:
                            latest_pub_date = published_at
                return news_list, latest_pub_date
            except Exception as e:
                logger.error(
                    f"[GOOGLE RSS FEED ERROR] Error Parsing for Ticker {ticker.symbol} - {e}"
                )
                logger.error(response.content)
        return [], None
