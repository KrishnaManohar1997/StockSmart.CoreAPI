from datetime import datetime, timezone
from common.constants.karma_bonus_intent import KarmaBonusIntent

from smallcase.api import SmallcaseManager
from smallcase.helper.smallcase_jwt_helper import SmallcaseJWTHelper
from user.models import UserHolding
from user.repositories import UserHoldingRepository
from smallcase.serializers import UserHoldingSerializer
from user.services.user_service import UserService


class UserHoldingService:
    smallcase_manager = SmallcaseManager()
    user_holding_repo = UserHoldingRepository()
    user_service = UserService()
    # 6 Hours in Seconds
    HOLDING_REFRESH_FREQUENCY = 21600

    def get_user_holding_or_none(self, user):
        try:
            return user.userholding
        except UserHolding.DoesNotExist:
            return None

    def __parse_smallcase_holdings_response_data(
        self, holdings_data: dict, is_update: bool = False
    ):
        # Schema Reference
        """{
            "smallcases": {
                "public": [],
                "private": {"stats": {"currentValue": 0, "totalReturns": 0}},
            },
            "securities": {"holdings": []},
            "lastUpdate": "2021-09-01T02:23:21.322Z",
            datetime.strptime('2021-09-01T02:23:21.322Z','%Y-%m-%dT%H:%M:%S.%fZ')
            "snapshotDate": "2021-09-01T02:23:21.322Z"
            "broker": "angelbroking", Doesn't exist while Update/Webhook
        }
        """
        stocksmart_user_holdings_data = {
            "holdings": {
                "smallcases": holdings_data["smallcases"],
                "securities": holdings_data["securities"],
            },
            "last_update": holdings_data["lastUpdate"],
        }
        if not is_update:
            stocksmart_user_holdings_data["broker_name"] = holdings_data["broker"]
        return stocksmart_user_holdings_data

    def create_user_holdings(self, user, holdings_data: dict):
        holdings_dict = self.__parse_smallcase_holdings_response_data(holdings_data)
        holdings_dict["user_id"] = str(user.id)
        self.user_service.assign_karma_bonus(
            user, KarmaBonusIntent.AUTHORIZE_HOLDINGS_IMPORT
        )
        return self.user_holding_repo.create_user_holdings(holdings_dict)

    def update_user_holdings(self, user_holding, holdings_data: dict):
        if user_holding.last_update == holdings_data["lastUpdate"]:
            return user_holding
        holdings_dict = self.__parse_smallcase_holdings_response_data(
            holdings_data, True
        )
        return self.user_holding_repo.update_user_holdings(
            user_holding, holdings_dict["holdings"], holdings_dict["last_update"]
        )

    def fetch_user_holdings(self, user):
        if not user.is_broker_connected():
            return False, "Please Connect to your broker to fetch holdings"

        user_holding = self.get_user_holding_or_none(user)
        if user_holding:
            # Add the Condition to enable autorefresh
            # and (datetime.now(timezone.utc) - user_holding.last_update).total_seconds()
            # >= self.HOLDING_REFRESH_FREQUENCY
            return True, UserHoldingSerializer(user_holding).data

        # Holdings Refresh Happens with Webhook
        smallcase_auth_token = SmallcaseJWTHelper.get_smallcase_jwt(
            user.smallcase_auth_id
        )

        smallcase_holdings_response = self.smallcase_manager.fetch_user_holdings(
            smallcase_auth_token
        )
        holdings_response_data = smallcase_holdings_response.json()["data"]
        if not user_holding:
            user_holding = self.create_user_holdings(user, holdings_response_data)
        else:
            user_holding = self.update_user_holdings(
                user_holding, holdings_response_data
            )
        return True, UserHoldingSerializer(user_holding).data
