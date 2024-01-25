from django.urls import path

from event_calendar.views import EventCalendarView

# v1/calendar-events/
urlpatterns = [
    # v1/calendar-events/
    path("", EventCalendarView.as_view()),
]
