from rest_framework.permissions import IsAuthenticated

from common.base_view import BaseView
from user.models import UserFriendship
from user.permissions import IsUserFriendshipActionValid
from user.services import UserFriendshipService


class UnfollowUserView(BaseView):
    permission_classes = [IsAuthenticated, IsUserFriendshipActionValid]
    user_friendship_service = UserFriendshipService()

    def post(self, request, social_user_id: str):
        (
            is_action_success,
            message,
        ) = self.user_friendship_service.perform_friendship_action(
            UserFriendship.UserFriendshipType.NO_FRIENDSHIP,
            request.user,
            social_user_id,
        )
        if is_action_success:
            return self.success_response(message=message)
        return self.bad_request_response(message=message)
