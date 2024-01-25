from user.services import UserHoldingService
from common.base_view import BaseView


class UserHoldingsView(BaseView):
    user_holding_service = UserHoldingService()

    def get(self, request):
        (
            is_success,
            user_holding_data,
        ) = self.user_holding_service.fetch_user_holdings(request.user)
        if not is_success:
            return self.bad_request_response(message=user_holding_data)
        return self.data_response(
            message=f"User Holdings",
            data=user_holding_data,
        )
