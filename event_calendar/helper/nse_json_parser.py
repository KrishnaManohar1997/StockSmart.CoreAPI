from datetime import datetime, timezone
from urllib.parse import parse_qsl, urlparse

import structlog

from common.helper.text_sanitizer import sanitize_text
from event_calendar.models import EventCalendar

logger = structlog.getLogger("django.server")


class NSEJsonParser:
    @staticmethod
    def parse_nse_event_data(nse_event_data: list):
        """
        {
            "symbol": "HAL",
            "company": "Hindustan Aeronautics Limited",
            "purpose": "Stock Split",
            "bm_desc": "To consider stock split of equity shares",
            "date": "21-Sep-2021",
        }
        """
        event_list, symbol_list, published_dates = [], [], []
        for event_dict in nse_event_data:
            symbol = event_dict["symbol"]
            published_data = datetime.strptime(event_dict["date"], "%d-%b-%Y").replace(
                tzinfo=timezone.utc
            )
            event_list.append(
                {
                    "symbol": symbol,
                    "purpose": event_dict["purpose"],
                    "description": event_dict["bm_desc"],
                    "published_at": published_data,
                    "attachment_url": None,
                    "event_type": EventCalendar.EventType.NSE_TICKER_EVENT,
                    "source_id": None,
                }
            )
            symbol_list.append(symbol)
            published_dates.append(published_data)
        return event_list, published_dates, symbol_list

    @staticmethod
    def nse_corporate_announcement_parser(announcement_data: list):
        """
        [{
            "symbol": "RELIANCE",
            "desc": "Shareholders meeting",
            "dt": "19092021190504",
            "attchmntFile": "https://archives.nseindia.com/corporate/RELIANCE_19092021190504_RILSEIntimationPostalBallotNotice.pdf",
            "sm_name": "Reliance Industries Limited",
            "sm_isin": "INE002A01018",
            "an_dt": "19-Sep-2021 19:05:04",
            "sort_date": "2021-09-19 19:05:04",
            "seq_id": "105078322",
            "smIndustry": "Refineries",
            "orgid": None,
            "attchmntText": "Please find attached the Postal Ballot Notice dated September 18, 2021, seeking approval of the members of the Company, by way of remote e-voting process, for appointment of His Excellency Yasir Othman H. Al Rumayyan (DIN: 09245977) as an Independent Director of the Company.ￂﾠPostal Ballot Notice is being sent only through electronic mode to the members whose names appear in the Register of Members / List of Beneficial Owners as received from National Securities Depository Limited and Central Depository Services (India) Limited and whose email ID is registered with the Company / Depositories, as on Friday, September 17, 2021 ( Cut-off Date ).ￂﾠThe Company has engaged the services of KFin Technologies Private Limited, Registrar and Transfer Agent, for providing remote e-voting facility to all its members. The e-voting facility will be available during the following period:ￂﾠCommencement of e-voting: 9:00 a.m. (IST) on Monday, September 20, 2021End of e-voting: 5:00 p.m. (IST) on Tuesday, October 19, 2021",
            "bflag": None,
            "old_new": None,
            "csvName": None,
            "exchdisstime": "19-Sep-2021 19:05:09",
            "difference": "00:00:05",
        }]
        """
        parsed_announcement_list, seq_id_list, symbol_list = [], [], []
        for announcement in announcement_data:
            source_id = announcement["seq_id"]
            symbol = announcement["symbol"]
            parsed_announcement_list.append(
                {
                    "symbol": symbol,
                    "purpose": announcement["desc"],
                    "description": announcement["attchmntText"],
                    "published_at": datetime.strptime(
                        announcement["an_dt"], "%d-%b-%Y %H:%M:%S"
                    ).astimezone(timezone.utc),
                    "attachment_url": announcement["attchmntFile"],
                    "source_id": source_id,
                    "event_type": EventCalendar.EventType.NSE_TICKER_ANNOUNCEMENT,
                }
            )
            seq_id_list.append(source_id)
            symbol_list.append(symbol)
        return parsed_announcement_list, seq_id_list, symbol_list

    @staticmethod
    def nse_corporate_announcement_rss_parser(announcement_data: list):
        """
        {
            "title": "Ester Industries Limited - Updates",
            "link": "http://feedproxy.google.com/~r/nseindia/ann/~3/XIunZLVHY-Q/AnnouncementDetail.jsp",
            "pubDate": "Sat, 09 Oct 2021 06:12:42 PST",
            "description": 'Ester Industries Limited has informed the Exchange regarding \'Pursuant to Regulation 74 (5) of SEBI (Depositories and Participants) Regulations, 2018, we areenclosing herewith the details of Dematerialised shares (as provided by......<div class="feedflare">\n<a href="http://feeds.feedburner.com/~ff/nseindia/ann?a=XIunZLVHY-Q:8inUQZwcfXU:7Q72WNTAKBA"><img src="http://feeds.feedburner.com/~ff/nseindia/ann?d=7Q72WNTAKBA" border="0"></img></a> <a href="http://feeds.feedburner.com/~ff/nseindia/ann?a=XIunZLVHY-Q:8inUQZwcfXU:gIN9vFwOqvQ"><img src="http://feeds.feedburner.com/~ff/nseindia/ann?i=XIunZLVHY-Q:8inUQZwcfXU:gIN9vFwOqvQ" border="0"></img></a> <a href="http://feeds.feedburner.com/~ff/nseindia/ann?a=XIunZLVHY-Q:8inUQZwcfXU:qj6IDK7rITs"><img src="http://feeds.feedburner.com/~ff/nseindia/ann?d=qj6IDK7rITs" border="0"></img></a> <a href="http://feeds.feedburner.com/~ff/nseindia/ann?a=XIunZLVHY-Q:8inUQZwcfXU:yIl2AUoC8zA"><img src="http://feeds.feedburner.com/~ff/nseindia/ann?d=yIl2AUoC8zA" border="0"></img></a>\n</div><img src="http://feeds.feedburner.com/~r/nseindia/ann/~4/XIunZLVHY-Q" height="1" width="1" alt=""/>',
            "feedburner:origLink": "http://nseindia.com/corporates/corpInfo/equities/AnnouncementDetail.jsp?symbol=ESTER&desc=Updates&tstamp=091020211842&",
        }
        """
        parsed_announcement_list, symbol_list = [], []
        if "item" in announcement_data["rss"]["channel"]:
            try:
                for news_item in announcement_data["rss"]["channel"]["item"]:
                    symbol = dict(
                        parse_qsl(urlparse(news_item["guid"]["#text"]).query)
                    ).get("symbol")
                    if not symbol:
                        continue
                    title_details = news_item["title"].rsplit("-")
                    if len(title_details) == 2:
                        purpose = title_details[1]
                    else:
                        continue
                    symbol_list.append(symbol)
                    parsed_announcement_list.append(
                        {
                            "symbol": symbol,
                            "purpose": purpose,
                            "description": sanitize_text(
                                news_item["description"], strip_data=True
                            ),
                            "published_at": datetime.strptime(
                                news_item["pubDate"], "%a, %d %b %Y %H:%M:%S PST"
                            ).replace(tzinfo=timezone.utc),
                            "attachment_url": None,
                            "source_id": None,
                            "event_type": EventCalendar.EventType.NSE_TICKER_ANNOUNCEMENT,
                        }
                    )
            except Exception as e:
                logger.info(e)
        return parsed_announcement_list, symbol_list
