import structlog
from django.core.exceptions import ValidationError

from common.helper.readable_serializer_error_translator import (
    translate_serializer_errors,
)
from smallcase.api import SmallcaseManager
from smallcase.helper.smallcase_jwt_helper import SmallcaseJWTHelper
from smallcase.models import Smallcase
from smallcase.repositories import SmallcaseRepository
from smallcase.serializers.smallcase_serializer import CreateSmallcaseSerializer
from stock.services import StockService

logger = structlog.getLogger("django.server")


class SmallcaseService:
    smallcase_manager = SmallcaseManager()
    smallcase_repo = SmallcaseRepository()
    stock_service = StockService()

    def get_all_smallcases(self):
        return self.smallcase_repo.get_all_smallcases()

    def get_smallcase_by_symbol_or_none(self, symbol):
        symbol = symbol.upper()
        try:
            return self.smallcase_repo.get_smallcase_by_symbol(symbol)
        except Smallcase.DoesNotExist:
            return None

    def get_smallcase_by_id_or_none(self, smallcase_id):
        try:
            return self.smallcase_repo.get_smallcase_by_id(smallcase_id)
        except Smallcase.DoesNotExist:
            return None

    def discover_all_smallcases(self) -> list:
        """Returns all the smallcases as a list
        from Smallcase API

        Returns:
            list: List of smallcase(s) dict
        """
        smallcase_response = self.smallcase_manager.discover_smallcases(
            SmallcaseJWTHelper.get_stocksmart_logged_jwt_token()
        )
        return smallcase_response.json()["data"]["smallcases"]

    def fetch_smallcase_details(self, smallcase_symbol: str) -> dict:
        """Get details of Smallcase from API

        Args:
            smallcase_symbol (str): scid (Smallcase Id)

        Returns:
            dict: Details of Smallcase
        """
        smallcase_response = self.smallcase_manager.fetch_smallcase_details(
            smallcase_symbol,
            SmallcaseJWTHelper.get_stocksmart_logged_jwt_token(),
        )
        return smallcase_response.json()["data"]

    def smallcase_constituents_mapper(self, constituents: list):
        stock_symbol_industry_map = dict(
            self.stock_service.get_all_stocks().values_list("symbol", "industry")
        )
        for constituent in constituents:
            constituent["industry"] = stock_symbol_industry_map[constituent["ticker"]]
        return constituents

    def get_stocksmart_smallcase_format(self, smallcase_details: dict) -> dict:
        try:
            smallcase_info = smallcase_details["info"]
            smallcase_stats = smallcase_details["stats"]
            smallcase_ratios = smallcase_stats["ratios"]
            return {
                "symbol": smallcase_details["scid"],
                "name": smallcase_info["name"],
                "publisher_name": smallcase_info["publisherName"],
                "description": smallcase_info["shortDescription"],
                "last_rebalanced": smallcase_info["lastRebalanced"],
                "logo_url": smallcase_info["imageUrl"],
                "returns": smallcase_stats["returns"],
                "index_value": smallcase_stats["indexValue"],
                "minimum_investment": smallcase_stats["minInvestAmount"],
                "cagr": smallcase_ratios["cagr"] * 100,
                "risk_percentage": smallcase_ratios["risk"],
                "price_52_week_high": round(smallcase_ratios["52wHigh"], 2),
                "price_52_week_low": round(smallcase_ratios["52wLow"], 2),
                "risk_label": smallcase_ratios["riskLabel"],
                "constituents": self.smallcase_constituents_mapper(
                    smallcase_details["constituents"]
                ),
            }
        except Exception as e:
            logger.error(
                f"Error Parsing Smallcase Details {e}",
                smallcase_details=smallcase_details,
            )

    def create_smallcase(self, smallcase_data: list, multi=False):
        if multi:
            smallcase_serializer = CreateSmallcaseSerializer(
                data=smallcase_data, many=True
            )
        else:
            smallcase_serializer = CreateSmallcaseSerializer(data=smallcase_data)

        if smallcase_serializer.is_valid():
            return smallcase_serializer.save()
        raise ValidationError(
            [
                translate_serializer_errors(error)
                for error in smallcase_serializer.errors
            ],
            code=400,
        )

    def load_db_with_smallcase_data(self):
        # ! Should be Used Only once to store all smallcases in DB
        smallcase_data = [
            self.get_stocksmart_smallcase_format(
                self.fetch_smallcase_details(smallcase["scid"])
            )
            for smallcase in self.discover_all_smallcases()
            if smallcase["scid"] not in ["WINMO_0001", "WINMO_0003"]
        ]
        self.create_smallcase(smallcase_data, multi=True)

    def fetch_smallcase_news(self, smallcase) -> list:
        """Fetches news for smallcase by Smallcase Id

        Args:
            smallcase (Smallcase): Smallcase Object

        Returns:
            list: List of smallcase news Dict
        """
        smallcase_news_response = self.smallcase_manager.fetch_smallcase_news(
            smallcase.symbol, SmallcaseJWTHelper.get_stocksmart_logged_jwt_token()
        )
        return smallcase_news_response.json().get("data")

    def get_smallcases_by_symbols(self, smallcase_symbols: list):
        return self.smallcase_repo.get_smallcases_by_symbols(smallcase_symbols)

    def update_all_smallcases(self):
        smallcases = self.smallcase_repo.get_all_smallcases()
        updated_smallcase_objects = []
        for smallcase in smallcases:
            smallcase_symbol = smallcase.symbol
            try:
                smallcase_details = self.get_stocksmart_smallcase_format(
                    self.fetch_smallcase_details(smallcase_symbol)
                )
                smallcase_details.pop("symbol")
                for (key, value) in smallcase_details.items():
                    setattr(smallcase, key, value)
                updated_smallcase_objects.append(smallcase)
                logger.info(f"Successfully Updated Smallcase {smallcase_symbol}")
            except Exception as error:
                logger.error(f"Failed Updating Smallcase {smallcase_symbol} -{error}")
        update_field_keys = list(smallcase_details.keys())
        Smallcase.objects.bulk_update(updated_smallcase_objects, update_field_keys)
        logger.info("Updated All Smallcases")
