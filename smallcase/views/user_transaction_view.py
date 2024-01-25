from common.base_view import BaseView
from smallcase.services import SmallcaseTransactionService


class UserTransactionView(BaseView):
    smallcase_transaction_service = SmallcaseTransactionService()

    def post(self, request):
        (
            is_success,
            response,
        ) = self.smallcase_transaction_service.user_transaction_resolver(request)
        if not is_success:
            return self.bad_request_response(message=response)

        response_json = response.json()
        return self.data_response(
            message=f"Transaction Id generated successfully",
            data=response_json["data"],
        )
