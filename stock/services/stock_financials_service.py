from django.forms import ValidationError
import structlog
from stock.constants import FinancialType, StockIncomePeriod

from stock.repositories import StockFinancialRepository

logger = structlog.getLogger("django.server")


class StockFinancialsService:
    stock_financial_repo = StockFinancialRepository()

    def get_stock_income_statement(self, stock, period: str = None):
        return self.stock_financial_repo.get_stock_income_statement(
            stock, FinancialType.INCOME_STATEMENT, period
        )

    def get_stock_balancesheet(self, stock):
        return self.stock_financial_repo.get_stock_balancesheet(
            stock, FinancialType.BALANCE_SHEET
        )

    def get_stock_cashflow(self, stock):
        return self.stock_financial_repo.get_stock_cashflow(
            stock, FinancialType.CASH_FLOW
        )

    def financials_filter(self, stock, request):
        statement_type = "statement"
        statement_period = "period"
        statement = request.query_params.get(
            statement_type, FinancialType.INCOME_STATEMENT
        )
        if statement == FinancialType.BALANCE_SHEET:
            return self.get_stock_balancesheet(stock)
        elif statement == FinancialType.CASH_FLOW:
            return self.get_stock_cashflow(stock)
        # Making Incomer Statement as Default
        period = request.query_params.get(statement_period, None)
        if period != None and period not in ["annual", "quarterly"]:
            raise ValidationError("Invalid period")
        return self.get_stock_income_statement(stock, period)
