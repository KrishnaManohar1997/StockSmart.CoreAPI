from smallcase.api import SmallcaseManager
from smallcase.constants import TransactionIntent
from smallcase.helper.smallcase_jwt_helper import SmallcaseJWTHelper


class SmallcaseTransactionService:
    smallcase_manager = SmallcaseManager()

    def user_transaction_resolver(self, request):
        transaction_intent = request.data.get("transaction_intent")
        if not (TransactionIntent.has_value(transaction_intent)):
            return False, "Invalid Intent"

        user = request.user
        if transaction_intent == TransactionIntent.CONNECT.value:
            return self.get_user_connect_transaction_id(user)

        # Except CONNECT, all transactions in Stock Smart need smallcase auth id
        if not user.is_broker_connected():
            return False, "Please connect to broker to perform the requested action"

        smallcase_auth_token = SmallcaseJWTHelper.get_smallcase_jwt(
            user.smallcase_auth_id
        )
        if transaction_intent == TransactionIntent.HOLDINGS_IMPORT.value:
            if user.is_import_holdings_authorized():
                return False, "Import Holdings is already Authorized"

            return self.get_user_holdings_import_transaction_id(smallcase_auth_token)

        elif transaction_intent == TransactionIntent.TRANSACTION.value:
            return self.get_order_transaction_id(
                smallcase_auth_token, request.data.get("order_config")
            )
        return False, "Transaction is invalid"

    def get_user_connect_transaction_id(self, user):
        if user.smallcase_auth_id:
            return False, "Invalid for broker-logged User"
        smallcase_auth_token = SmallcaseJWTHelper.get_smallcase_jwt()
        return True, self.smallcase_manager.get_connect_transaction_id(
            smallcase_auth_token
        )

    def get_user_holdings_import_transaction_id(self, smallcase_auth_token):
        return True, self.smallcase_manager.fetch_holdings_transaction_id(
            smallcase_auth_token
        )

    def get_order_transaction_id(
        self, smallcase_auth_token: str, order_config: dict = None
    ):
        return True, self.smallcase_manager.create_order_transaction_id(
            smallcase_auth_token, order_config
        )
