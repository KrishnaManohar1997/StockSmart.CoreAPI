from django.core.management.base import BaseCommand
from event_calendar.services import EventCalendarService


class Command(BaseCommand):
    help = "Resets the database"

    def handle(self, *args, **options):
        EventCalendarService().sync_nse_calendar_events(True)
