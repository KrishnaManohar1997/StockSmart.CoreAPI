from django.core.management.base import BaseCommand

from smallcase.services.smallcase_service import SmallcaseService


class Command(BaseCommand):
    help = "Updates all Smallcase Details"

    def handle(self, *args, **options):
        # Fetches all Smallcases and writes them to db
        SmallcaseService().update_all_smallcases()
