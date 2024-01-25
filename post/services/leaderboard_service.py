from datetime import timedelta

from common.helper.datetime_helper import DateTimeHelper
from post.repositories import LeaderboardRepository
from post.serializers import LeaderboardSerializer
from django.core.cache import cache

LEADERBOARD_USERS_KEY = "LEADERBOARD_USERS"


class LeaderboardService:
    leaderboard_repo = LeaderboardRepository()

    def bulk_create_items(self, leaderboard_objs):
        return self.leaderboard_repo.bulk_create_items(leaderboard_objs)

    def get_leaderboard_on_date(self, date):
        return self.leaderboard_repo.get_leaderboard_on_day(date)

    def update_leaderboard_users_data_day(self, date, update_cache=False, ttl=6000):
        data = LeaderboardSerializer(self.get_leaderboard_on_date(date), many=True).data
        if not data:
            data = {}
        data = {
            "rewards": self.leaderboard_repo.get_total_rewards(),
            "date": date,
            "data": data,
        }
        if update_cache:
            cache.set(LEADERBOARD_USERS_KEY, data, timeout=ttl)
        return data

    def get_today_leaderboard(self):
        today_leaderboard_data = cache.get(LEADERBOARD_USERS_KEY)
        if today_leaderboard_data:
            return today_leaderboard_data
        now = today = DateTimeHelper.get_asia_calcutta_time_now()
        leaderboard_sync_time = now.replace(hour=17, minute=0, second=0)
        next_leaderboard_sync_time = leaderboard_sync_time + timedelta(days=1)
        ttl = (next_leaderboard_sync_time - now).seconds
        if today >= leaderboard_sync_time:
            return self.update_leaderboard_users_data_day(today.date(), True, ttl)

        prev_leaderboard_sync_time = leaderboard_sync_time - timedelta(days=1)
        return self.update_leaderboard_users_data_day(
            prev_leaderboard_sync_time.date(), True, ttl
        )
