from common.base_view import BaseView
from smallcase.helper.smallcase_jwt_helper import SmallcaseJWTHelper
from user.services import UserService
import structlog

logger = structlog.getLogger("django.server")


class UpdateUserSmallcaseAuthIdView(BaseView):
    user_service = UserService()

    def post(self, request):
        SMALLCASE_AUTHTOKEN_KEY = "smallcase_auth_token"
        if SMALLCASE_AUTHTOKEN_KEY not in request.data:
            return self.bad_request_response(message="Required parameters missing")
        try:
            smallcase_auth_id = SmallcaseJWTHelper.extract_smallcase_auth_id(
                request.data.get(SMALLCASE_AUTHTOKEN_KEY)
            )
        except Exception as error:
            logger.error(f"Invalid JWT for Updating Smallcase Token -> {error}")
            return self.bad_request_response(
                "Invalid Data, Please try Connecting with Broker again"
            )
        if not smallcase_auth_id:
            return self.bad_request_response(
                message="Invalid token, Please login with broker to continue"
            )
        is_valid, obj = self.user_service.ingest_smallcase_auth_id(
            request.user, smallcase_auth_id
        )
        if not is_valid:
            return self.bad_request_response(obj)
        return self.success_response(message="Smallcase auth id stored successfully")
