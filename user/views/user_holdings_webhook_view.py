import structlog

from common.base_view import PublicBaseView
from user.services import UserHoldingService, UserService

logger = structlog.getLogger("django.server")


class UserHoldingsWebhookView(PublicBaseView):
    user_holding_service = UserHoldingService()
    user_service = UserService()

    def post(self, request):
        holdings_data = request.data
        smallcase_auth_id = holdings_data.get("smallcaseAuthId")
        if holdings_data is None or not smallcase_auth_id:
            return self.bad_request_response("Invalid Request")

        user = self.user_service.get_user_by_smallcase_auth_id(smallcase_auth_id)

        if not user:
            logger.error(
                f"[USER HOLDING WEBHOOK] User Doesn't exist for with {smallcase_auth_id=}"
            )
        elif not user.is_import_holdings_authorized():
            self.user_holding_service.create_user_holdings(user, holdings_data)
        else:
            self.user_holding_service.update_user_holdings(
                user.userholding, holdings_data
            )
        return self.success_response("Ok")
