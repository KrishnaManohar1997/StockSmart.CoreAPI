from django.db import models


class StockIncomePeriod(models.TextChoices):
    ANNUAL = "annual"
    QUARTERLY = "quarterly"


class FinancialType(models.TextChoices):
    BALANCE_SHEET = "balancesheet"
    INCOME_STATEMENT = "income"
    CASH_FLOW = "cashflow"
