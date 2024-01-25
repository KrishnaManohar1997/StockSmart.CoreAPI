from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated

from common.base_view import BaseView
from common.helper.normalize_fk_serializer_data import normalize_fk_serializer_data
from user.permissions import IsBlockedByUser
from user.serializers import UserFriendshipFollowingSerializer
from user.services import UserFriendshipService


class UserFollowingListView(BaseView):
    permission_classes = [IsAuthenticated, IsBlockedByUser]
    user_friendship_service = UserFriendshipService()
    serializer = UserFriendshipFollowingSerializer
    paginator = LimitOffsetPagination()

    def post(self, request, social_user_id: str):
        followers_queryset = self.user_friendship_service.get_user_following_list(
            social_user_id
        )
        page = self.paginator.paginate_queryset(followers_queryset, request)
        data = self.serializer(page, many=True).data
        data = normalize_fk_serializer_data(data)
        return self.paginated_response(self.paginator, "Following Users", data)
