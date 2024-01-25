from smallcase.serializers import (
    SmallcaseDetailsSerializer,
    AnonymousUserSmallcaseDetailsSerializer,
)
from common.base_view import PublicBaseView
from smallcase.services import SmallcaseService


class SmallcaseView(PublicBaseView):
    smallcase_service = SmallcaseService()

    def get(self, request, smallcase_symbol: str):
        smallcase = self.smallcase_service.get_smallcase_by_symbol_or_none(
            smallcase_symbol
        )
        if not smallcase:
            return self.bad_request_response("Invalid request")
        user = request.user
        serializer = (
            SmallcaseDetailsSerializer
            if user.is_authenticated and user.smallcase_auth_id
            else AnonymousUserSmallcaseDetailsSerializer
        )
        smallcase_data = serializer(smallcase).data
        return self.data_response(message="Smallcase Data", data=smallcase_data)
