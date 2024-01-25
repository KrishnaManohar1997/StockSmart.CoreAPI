from datetime import datetime

from user.models import UserHolding


class UserHoldingRepository:
    def create_user_holdings(self, user_holding: dict):
        return UserHolding.objects.create(**user_holding)

    def update_user_holdings(
        self, user_holding: UserHolding, holdings_dict: dict, last_update: datetime
    ):
        user_holding.holdings = holdings_dict
        user_holding.last_update = last_update
        user_holding.save()
        return user_holding

    def get_user_holding(self, user_id):
        return UserHolding.objects.get(user_id=user_id)
