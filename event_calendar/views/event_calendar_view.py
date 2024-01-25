from event_calendar.services import EventCalendarService
from event_calendar.serializers import EventCalendarSerializer
from common.base_view import PublicBaseView


class EventCalendarView(PublicBaseView):
    serializer = EventCalendarSerializer
    event_calendar_service = EventCalendarService()

    def get(self, request):
        return self.data_response(
            message="Ok",
            data=self.serializer(
                self.event_calendar_service.get_stocksmart_calendar(), many=True
            ).data,
        )
