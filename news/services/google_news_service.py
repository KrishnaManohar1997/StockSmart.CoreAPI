from news.api import GoogleNewsRssManager


class GoogleNewsService:
    news_rss_manager = GoogleNewsRssManager()

    def get_ticker_news(self, ticker):
        news_list, latest_pub_date = self.news_rss_manager.get_ticker_news(ticker)
        return news_list, latest_pub_date
