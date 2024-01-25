from post.models import Leaderboard
from django.db.models import Sum


class LeaderboardRepository:
    def bulk_create_items(self, leaderboard_objs):
        return Leaderboard.objects.bulk_create(leaderboard_objs)

    def get_leaderboard_on_day(self, date):
        return Leaderboard.objects.filter(date=date).prefetch_related("post", "user")

    def get_total_rewards(self):
        return Leaderboard.objects.aggregate(Sum("reward"))["reward__sum"]
