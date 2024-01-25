import requests
import xmltodict

from event_calendar.exceptions import NSEResponseHandler


class NSEManager:
    BASE_URL = "https://www.nseindia.com/api"
    NSE_INDIA_RSS_BASE_URL = "http://feeds.feedburner.com/nseindia"
    NSE_TIMEOUT = 5

    def __generate_cookie_for_nse(self, nse_page: str = None):
        nse_session = requests.Session()
        nse_session.headers[
            "User-Agent"
        ] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36"
        nse_page = (
            nse_page
            or "https://www.nseindia.com/companies-listing/corporate-filings-financial-results"
        )
        nse_session.get(nse_page)
        cookie_jar = nse_session.cookies
        generated_cookie = ""
        for cookie in cookie_jar:
            if isinstance(cookie.value, str):
                generated_cookie += f"{cookie.name}={cookie.value};"
        return generated_cookie

    def __get_nse_headers(self):
        return {
            "authority": "www.nseindia.com",
            "cache-control": "max-age=0",
            "sec-ch-ua": '"Google Chrome";v="93"," Not;A Brand";v="99","Chromium";v="93"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "sec-fetch-site": "cross-site",
            "sec-fetch-mode": "navigate",
            "sec-fetch-user": "?1",
            "sec-fetch-dest": "document",
            "accept-language": "en-US,en;q=0.9",
            "cookie": self.__generate_cookie_for_nse(),
        }

    def get_nse_corporate_announcements_rss(self):
        announcement_response = requests.get(
            url=f"{self.NSE_INDIA_RSS_BASE_URL}/ann",
            timeout=self.NSE_TIMEOUT,
        )
        NSEResponseHandler.handle_response(announcement_response)

        return xmltodict.parse(announcement_response.content)

    def get_nse_corporate_announcements(self, index_type: str = "equities"):
        params = {"index": index_type}
        announcement_response = requests.get(
            url=f"{self.BASE_URL}/corporate-announcements",
            headers=self.__get_nse_headers(),
            params=params,
            timeout=self.NSE_TIMEOUT,
        )
        NSEResponseHandler.handle_response(announcement_response)
        return announcement_response.json()

    def get_nse_event_calendar(self, start_date: str, end_date: str):
        params = {"from_date": start_date, "to_date": end_date}
        events_response = requests.get(
            url=f"{self.BASE_URL}/event-calendar",
            params=params,
            headers=self.__get_nse_headers(),
            timeout=self.NSE_TIMEOUT,
        )
        NSEResponseHandler.handle_response(events_response)
        return events_response.json()
