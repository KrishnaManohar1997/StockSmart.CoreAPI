from event_calendar.models import EventCalendar


class EventCalendarRepository:
    def get_stocksmart_calendar(self, start_date, end_date):
        return (
            EventCalendar.objects.filter(
                published_at__gte=start_date,
                published_at__lte=end_date,
                event_type__in=[
                    EventCalendar.EventType.NSE_TICKER_ANNOUNCEMENT,
                    EventCalendar.EventType.NSE_TICKER_EVENT,
                ],
            )
            .prefetch_related("symbol")
            .order_by("-published_at")
        )

    def get_announcements_by_source_ids(self, source_ids):
        return EventCalendar.objects.filter(source_id__in=source_ids)

    def get_nse_calendar_events_by_published_dates(self, published_dates, symbol_list):
        return EventCalendar.objects.filter(
            event_type=EventCalendar.EventType.NSE_TICKER_EVENT,
            published_at__in=published_dates,
            symbol__symbol__in=symbol_list,
        ).select_related("symbol")

    def bulk_insert_calendar_events(
        self, event_calendar_objects: list, ignore_conflicts: bool = False
    ):
        return EventCalendar.objects.bulk_create(
            event_calendar_objects, ignore_conflicts=ignore_conflicts
        )

    def get_nse_recent_announcement(self):
        return (
            EventCalendar.objects.filter(
                event_type=EventCalendar.EventType.NSE_TICKER_ANNOUNCEMENT
            )
            .order_by("-created_at")
            .first()
        )

    def get_nse_recent_ticker_event(self):
        return (
            EventCalendar.objects.filter(
                event_type=EventCalendar.EventType.NSE_TICKER_EVENT
            )
            .order_by("-created_at")
            .first()
        )
