from django.db.models import Sum

from common.base_view import BaseView
from post.serializers.leaderboard_serializer import LeaderboardNotificationSerializer
from user.services import UserService


class UserRewardsView(BaseView):
    user_service = UserService()

    def get(self, request):
        leaderboard_qs = self.user_service.get_user_rewards(request.user)
        return self.data_response(
            "Leaderboard Rewards",
            data={
                "total_rewards": 0
                if not leaderboard_qs
                else leaderboard_qs.aggregate(Sum("reward"))["reward__sum"],
                "leaderboard": LeaderboardNotificationSerializer(
                    leaderboard_qs, many=True
                ).data,
            },
        )
