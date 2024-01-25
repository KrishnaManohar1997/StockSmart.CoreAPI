from common.base_view import BaseView
from user.serializers import UserFriendshipFollowerSerializer
from user.services import UserFriendshipService, UserService
from rest_framework.pagination import LimitOffsetPagination


class UserFriendshipView(BaseView):
    user_friendship_service = UserFriendshipService()
    user_service = UserService()
    serializer = UserFriendshipFollowerSerializer
    paginator = LimitOffsetPagination()

    def post(self, request):
        if (
            not type(request.data) == dict and not request.data.get("user_ids")
        ) or type(request.data.get("user_ids")) != list:
            return self.bad_request_response("Required Parameter is missing")

        user_ids = request.data.get("user_ids")
        friendship_data = self.user_friendship_service.get_friendship_status_list(
            request.user, user_ids
        )
        return self.data_response(message="Friendship status", data=friendship_data)
