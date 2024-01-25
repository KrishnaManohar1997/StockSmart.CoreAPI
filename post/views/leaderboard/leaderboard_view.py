from common.base_view import PublicBaseView
from post.services import LeaderboardService


class LeaderboardView(PublicBaseView):
    leaderboard_service = LeaderboardService()

    def get(self, request):
        leaderboard_members = self.leaderboard_service.get_today_leaderboard()
        return self.data_response("", leaderboard_members)
