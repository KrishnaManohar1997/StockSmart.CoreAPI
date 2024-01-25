import json
from typing import Tuple

import requests
from django.conf import settings
from django.core.exceptions import ValidationError

from smallcase.constants import TransactionIntent
from smallcase.exceptions import SmallcaseResponseHandler

SMALLCASE_GATEWAY_NAME = settings.SMALLCASE_GATEWAY_NAME
SMALLCASE_GATEWAY_SECRET = settings.SMALLCASE_GATEWAY_SECRET
from stock.services import StockService


class SmallcaseManager:
    SMALLCASE_BASE_URL = "https://gatewayapi.smallcase.com"

    def __get_smallcase_stocksmart_engine_url(self):
        return f"{self.SMALLCASE_BASE_URL}/v1/{SMALLCASE_GATEWAY_NAME}/engine"

    def __get_stocksmart_gateway_url(self):
        return f"{self.SMALLCASE_BASE_URL}/gateway/{SMALLCASE_GATEWAY_NAME}"

    def __get_transaction_url(self):
        return f"{self.__get_stocksmart_gateway_url()}/transaction"

    def __get_smallcase_headers(self, user_jwt_auth_token):
        return {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "x-gateway-authtoken": user_jwt_auth_token,
            "x-gateway-secret": SMALLCASE_GATEWAY_SECRET,
        }

    def __is_smallcase_order_config_valid(self, order_config):
        order_type = order_config.get("type")
        if not order_type or order_type not in ["BUY", "EXIT"]:
            return False
        smallcase_id = order_config.get("scid")
        if not smallcase_id:
            return False
        return True

    def __is_security_order_config_valid(self, order_config):
        nse_ticker_symbols = []
        for security in order_config:
            ticker = security.get("ticker")
            if not ticker or not isinstance(ticker, str):
                return False
            # Creating Ticker list to validate
            nse_ticker_symbols.append(ticker.upper())

            quantity = security.get("quantity")
            if quantity and not isinstance(quantity, int):
                return False

            order_type = security.get("type")
            if order_type and (
                not isinstance(order_type, str) or order_type not in ["BUY", "SELL"]
            ):
                return False
        return StockService().get_stocks_by_symbols(nse_ticker_symbols).count() == len(
            nse_ticker_symbols
        )

    def __is_order_config_valid(self, order_config: list) -> Tuple[bool, str]:
        """Validates Order Config for Single Stock Order
        Refer -> https://developers.gateway.smallcase.com/reference/single-stock-transaction

        Args:
            order_config (list): List of Securities Order Config

        Returns:
            [bool,str]: True if the config is valid else False, Type of Order
            Smallcase or Security
        """
        # Only supporting Single Order Transaction for now
        if isinstance(order_config, list) and len(order_config) == 1:
            return self.__is_security_order_config_valid(order_config), "Security"
        elif isinstance(order_config, dict):
            return self.__is_smallcase_order_config_valid(order_config), "Smallcase"
        else:
            return False, None

    def __trigger_transaction(self, user_jwt_auth_token: str, data: dict):
        url = self.__get_transaction_url()
        headers = self.__get_smallcase_headers(user_jwt_auth_token)
        transaction_response = requests.post(url, headers=headers, json=data)
        SmallcaseResponseHandler.handle_response(transaction_response)
        return transaction_response

    def get_connect_transaction_id(self, user_jwt_auth_token: str):
        return self.__trigger_transaction(
            user_jwt_auth_token, data={"intent": TransactionIntent.CONNECT.value}
        )

    def fetch_holdings_transaction_id(self, user_jwt_auth_token: str):
        return self.__trigger_transaction(
            user_jwt_auth_token,
            data={"intent": TransactionIntent.HOLDINGS_IMPORT.value},
        )

    def create_order_transaction_id(
        self, user_jwt_auth_token: str, order_config: list = None
    ):
        data = {"intent": TransactionIntent.TRANSACTION.value}
        if order_config:
            is_valid, order_type = self.__is_order_config_valid(order_config)
            if not is_valid:
                raise ValidationError("Invalid Order details for Transaction", code=400)
            if order_type == "Security":
                data["orderConfig"] = {"type": "SECURITIES", "securities": order_config}
            elif order_type == "Smallcase":
                data["orderConfig"] = order_config
        return self.__trigger_transaction(user_jwt_auth_token, data)

    def fetch_user_holdings(self, user_jwt_auth_token: str):
        url = f"{self.__get_stocksmart_gateway_url()}/user/holdings"
        headers = self.__get_smallcase_headers(user_jwt_auth_token)
        user_holdings_response = requests.get(url, headers=headers)
        SmallcaseResponseHandler.handle_response(user_holdings_response)
        return user_holdings_response

    def discover_smallcases(self, user_jwt_auth_token: str):
        url = f"{self.__get_smallcase_stocksmart_engine_url()}/smallcases?count=100"
        headers = self.__get_smallcase_headers(user_jwt_auth_token)
        smallcases_response = requests.get(url, headers=headers)
        SmallcaseResponseHandler.handle_response(smallcases_response)
        return smallcases_response

    def fetch_smallcase_details(self, smallcase_id: str, user_jwt_auth_token: str):
        url = f"{self.__get_smallcase_stocksmart_engine_url()}/smallcase"
        headers = self.__get_smallcase_headers(user_jwt_auth_token)
        params = {"scid": smallcase_id}
        smallcases_response = requests.get(url, headers=headers, params=params)
        SmallcaseResponseHandler.handle_response(smallcases_response)
        return smallcases_response

    def fetch_smallcase_news(self, smallcase_id: str, user_jwt_auth_token: str):
        url = f"{self.__get_smallcase_stocksmart_engine_url()}/market/news"
        headers = self.__get_smallcase_headers(user_jwt_auth_token)
        params = {"scids[]": smallcase_id, "count": 10, "offset": 0}
        smallcases_response = requests.get(url, headers=headers, params=params)
        SmallcaseResponseHandler.handle_response(smallcases_response)
        return smallcases_response
