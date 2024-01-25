from common.base_view import PublicBaseView, BaseView
from smallcase.helper.smallcase_jwt_helper import SmallcaseJWTHelper


class GenerateUserSmallCaseTokenView(BaseView):
    def get(self, request):
        smallcase_auth_id = SmallcaseJWTHelper.get_smallcase_jwt(
            request.user.smallcase_auth_id
        )
        return self.data_response(
            message="Generated smallcase auth token", data=smallcase_auth_id
        )


class GenerateGuestSmallcaseTokenView(PublicBaseView):
    def get(self, request):
        smallcase_auth_token = SmallcaseJWTHelper.get_smallcase_jwt(None)
        return self.data_response(
            message="Generated smallcase auth token", data=smallcase_auth_token
        )
