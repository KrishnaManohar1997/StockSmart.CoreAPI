from datetime import datetime, timedelta, timezone

import structlog

from common.helper import DateTimeHelper
from event_calendar.api import NSEManager
from event_calendar.helper.nse_json_parser import NSEJsonParser
from event_calendar.models import EventCalendar
from event_calendar.repositories import EventCalendarRepository
from stock.services import StockService

logger = structlog.getLogger("django.server")


class EventCalendarService:
    event_calendar_repo = EventCalendarRepository()
    nse_manager = NSEManager()
    stock_service = StockService()
    nse_json_parser = NSEJsonParser
    # 10 Minutes in Seconds
    NSE_ANNOUNCEMENT_REFRESH_FREQUENCY = 600

    def __is_nse_refresh_needed(self, last_fetched_at) -> bool:
        if not last_fetched_at:
            return True
        return (
            datetime.now(timezone.utc) - last_fetched_at
        ).total_seconds() >= self.NSE_ANNOUNCEMENT_REFRESH_FREQUENCY

    def sync_nse_calendar_events(self, force_refresh=False):
        if not force_refresh:
            recent_ticker_event = self.get_nse_recent_ticker_event()
            if (
                recent_ticker_event
                and recent_ticker_event.created_at.date
                != datetime.now().replace(tzinfo=timezone.utc).date
            ):
                logger.info("No Sync Needed")
                return
        logger.info("Refreshing Events")

        # Getting Events for Tickers for next 1 week
        start_date = DateTimeHelper.get_asia_calcutta_time_now().strftime("%d-%m-%Y")
        end_date = (
            DateTimeHelper.get_asia_calcutta_time_now() + timedelta(days=7)
        ).strftime("%d-%m-%Y")

        ticker_events = self.nse_manager.get_nse_event_calendar(start_date, end_date)
        (
            ticker_event_data,
            published_dates,
            symbol_list,
        ) = self.nse_json_parser.parse_nse_event_data(ticker_events)
        existing_ticker_events = dict(
            self.get_nse_calendar_events_by_published_dates(
                published_dates, symbol_list
            ).values_list("symbol", "published_at")
        )
        symbols_dict = dict(
            self.stock_service.get_stocks_by_symbols(symbol_list).values_list(
                "symbol", "id"
            )
        )
        ticker_event_objects = []
        for ticker_event in ticker_event_data:
            symbol = ticker_event.pop("symbol")
            published_at_time = ticker_event.get("published_at")
            try:
                if existing_ticker_events.get(symbol) != published_at_time:
                    ticker_event["symbol_id"] = symbols_dict[symbol]
                    ticker_event_objects.append(EventCalendar(**ticker_event))
                else:
                    logger.info("existing")
            except Exception as error:
                logger.info(f"Error storing NSE Ticker Event, {error}")
        self.bulk_insert_calendar_events(ticker_event_objects, ignore_conflicts=True)

    def get_nse_calendar_events_by_published_dates(self, published_dates, symbol_list):
        return self.event_calendar_repo.get_nse_calendar_events_by_published_dates(
            published_dates, symbol_list
        )

    def sync_nse_announcements_rss(self):
        announcements_list = self.nse_manager.get_nse_corporate_announcements_rss()
        (
            announcements_parsed_data,
            symbol_list,
        ) = self.nse_json_parser.nse_corporate_announcement_rss_parser(
            announcements_list
        )
        symbols_dict = dict(
            self.stock_service.get_stocks_by_symbols(symbol_list).values_list(
                "symbol", "id"
            )
        )
        event_calendar_objects = []
        for announcement in announcements_parsed_data:
            try:
                announcement["symbol_id"] = symbols_dict[announcement.pop("symbol")]
                event_calendar_objects.append(EventCalendar(**announcement))
            except Exception as error:
                logger.info(f"Error storing NSE Announcement, {error}")
        self.bulk_insert_calendar_events(event_calendar_objects, ignore_conflicts=True)

    def sync_nse_announcements(self):
        recent_announcement = self.get_nse_recent_announcement()
        if recent_announcement and not self.__is_nse_refresh_needed(
            recent_announcement.created_at
        ):
            logger.info("No Refresh Needed")
            return
        logger.info("Refreshing Announcements")
        announcements_list = self.nse_manager.get_nse_corporate_announcements()
        (
            announcements_parsed_data,
            source_ids,
            symbol_list,
        ) = self.nse_json_parser.nse_corporate_announcement_parser(announcements_list)
        exclude_source_ids = list(
            self.get_announcements_by_source_ids(source_ids).values_list(
                "source_id", flat=True
            )
        )
        symbols_dict = dict(
            self.stock_service.get_stocks_by_symbols(symbol_list).values_list(
                "symbol", "id"
            )
        )
        event_calendar_objects = []
        for announcement in announcements_parsed_data:
            try:
                if announcement["source_id"] not in exclude_source_ids:
                    announcement["symbol_id"] = symbols_dict[announcement.pop("symbol")]
                    event_calendar_objects.append(EventCalendar(**announcement))
            except Exception as error:
                logger.info(f"Error storing NSE Announcement, {error}")
        self.bulk_insert_calendar_events(event_calendar_objects)

    def bulk_insert_calendar_events(
        self, event_calendar_objects: list, ignore_conflicts: bool = False
    ):
        return self.event_calendar_repo.bulk_insert_calendar_events(
            event_calendar_objects, ignore_conflicts
        )

    def get_announcements_by_source_ids(self, source_ids):
        return self.event_calendar_repo.get_announcements_by_source_ids(source_ids)

    def get_stocksmart_calendar(self):
        self.sync_nse_calendar_events()

        start_date = DateTimeHelper.get_asia_calcutta_time_now().replace(
            hour=00, minute=00, second=00, microsecond=00, tzinfo=timezone.utc
        )
        end_date = DateTimeHelper.get_asia_calcutta_time_now().replace(
            hour=23, minute=59, second=59, microsecond=00, tzinfo=timezone.utc
        ) + timedelta(days=7)
        return self.event_calendar_repo.get_stocksmart_calendar(start_date, end_date)

    def get_nse_recent_announcement(self):
        return self.event_calendar_repo.get_nse_recent_announcement()

    def get_nse_recent_ticker_event(self):
        return self.event_calendar_repo.get_nse_recent_ticker_event()
