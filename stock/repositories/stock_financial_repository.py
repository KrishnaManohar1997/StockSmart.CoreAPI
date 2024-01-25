class StockFinancialRepository:
    def get_stock_income_statement(self, stock, statement: str, period: str):
        income_statement = stock.financials.filter(statement=statement)
        if period:
            return income_statement.filter(period=period)
        return income_statement

    def get_stock_balancesheet(self, stock, statement: str):
        return stock.financials.filter(statement=statement)

    def get_stock_cashflow(self, stock, statement: str):
        return stock.financials.filter(statement=statement)
