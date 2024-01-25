from user.serializers.user_serializer import UserSearchSerializer
from rest_framework.pagination import LimitOffsetPagination

from common.base_view import PublicBaseView
from user.services import UserService


class UserSearchView(PublicBaseView):
    serializer = UserSearchSerializer
    user_service = UserService()
    paginator = LimitOffsetPagination()

    def get(self, request):
        username_query = request.query_params.get("q")
        if not username_query or not self.user_service.is_username_valid(
            username_query, min_length=1
        ):
            return self.bad_request_response("No search")
        user_queryset = self.user_service.get_users_by_username(
            username_query, request.user.id
        )
        if request.user.is_authenticated:
            user_queryset = user_queryset.exclude(
                id__in=self.user_service.get_blocked_by_user_ids(request.user.id)
            )
        page = self.paginator.paginate_queryset(user_queryset, request)
        data = self.serializer(page, many=True).data
        return self.paginated_response(self.paginator, "Users", data)
