from .twelve_data import TickerDataService


class TickerDataHelper:

    ticker_data_service = TickerDataService()

    def get_ticker_data_by_minute_interval(
        self, ticker_symbol: str, start_date, end_date, exchange: str = "NSE"
    ) -> dict:
        response = self.ticker_data_service.get_ticker_data_by_minute_interval(
            ticker_symbol, start_date, end_date
        )
        if response.status_code == 200:
            return {"is_valid": True, "data": response.json().get("values")}
        return {
            "is_valid": False,
            "message": f"API call Failed with status {response.status_code} -> {response.content}",
        }

    def get_quote_for_tickers_for_day(
        self, ticker_symbols: list, exchange: str = "NSE"
    ) -> dict:
        response = self.ticker_data_service.get_quote_for_tickers_for_day(
            ticker_symbols, exchange
        )
        print(response.json())
        if response.status_code == 200:
            return {"is_valid": True, "data": response.json().get("data")}
        return {
            "is_valid": False,
            "message": f"API call Failed with status {response.status_code} -> {response.content}",
        }
