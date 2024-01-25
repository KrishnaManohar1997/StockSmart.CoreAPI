from django.core.management.base import BaseCommand
from user.models import User
from watchlist.models import Watchlist


class Command(BaseCommand):
    help = "Creates Watchlists for All Users"

    def handle(self, *args, **options):
        watchlist_users = Watchlist.objects.all().values_list(
            "created_by_user_id", flat=True
        )
        watchlist_objects = [
            Watchlist(created_by_user=user)
            for user in User.objects.exclude(id__in=watchlist_users)
        ]
        Watchlist.objects.bulk_create(watchlist_objects)
        print("Created Watchlists for Old Users")
