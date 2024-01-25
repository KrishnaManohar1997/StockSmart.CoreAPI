from datetime import datetime, timedelta, timezone
from news.models import News


class NewsParser:
    @staticmethod
    def smallcase_news_parser(news_dict_list, smallcase):
        news_api_source = News.NewsAPISource.SMALLCASE
        news_articles, news_titles = [], []
        latest_pub_date = datetime.now(timezone.utc) - timedelta(days=50)
        for news_dict in news_dict_list:
            # Date format 2021-09-14T18:19:33.000Z
            published_at = datetime.strptime(
                news_dict["date"], "%Y-%m-%dT%H:%M:%S.%fZ"
            ).replace(tzinfo=timezone.utc)
            # Makes Sure that new news will be fetched
            if (
                # If doesn't have a latest published article date (None)
                not smallcase.latest_pub_news_date
                or
                # Check all articles are after the latest date
                smallcase.latest_pub_news_date < published_at
            ):
                news_titles.append(news_dict["headline"])
                news_articles.append(
                    {
                        "title": news_dict["headline"],
                        "description": news_dict["summary"],
                        "api_source": news_api_source,
                        "source_id": None,
                        "source_name": news_dict["publisher"]["name"],
                        "url": news_dict["link"],
                        "image_url": news_dict["imageUrl"],
                        "published_at": published_at,
                        "tickers": [stock["sid"] for stock in news_dict["stocks"]],
                    }
                )
                # Stores the most recent Published Date
                if published_at > latest_pub_date:
                    latest_pub_date = published_at
        return news_titles, news_articles, latest_pub_date

    @staticmethod
    def google_rss_news_parser(news_dict):
        return

    @staticmethod
    def news_api_news_parser(news_dict):
        return

    @staticmethod
    def parse_news_dict(news_dict, source: News.NewsAPISource, instance=None):
        if not instance and News.NewsAPISource.NEWS_API == source:
            return NewsParser.news_api_news_parser(news_dict)
        if News.NewsAPISource.SMALLCASE == source:
            return NewsParser.smallcase_news_parser(news_dict, instance)
        elif News.NewsAPISource.GOOGLE_RSS == source:
            return NewsParser.google_rss_news_parser(news_dict)
