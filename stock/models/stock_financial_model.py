from django.db import models

from common.models import BaseModel
from stock.constants import FinancialType, StockIncomePeriod

from . import Stock


class StockFinancial(BaseModel):
    stock = models.ForeignKey(
        Stock, on_delete=models.DO_NOTHING, related_name="financials"
    )
    period = models.CharField(
        max_length=16,
        null=True,
        blank=True,
        choices=StockIncomePeriod.choices,
        db_index=True,
    )
    fiscal_date = models.DateField(blank=False, null=False, db_index=True)
    data = models.JSONField(blank=False, null=False)
    created_by_user = None
    statement = models.CharField(
        max_length=16,
        null=True,
        blank=True,
        choices=FinancialType.choices,
        db_index=True,
    )

    class Meta:
        verbose_name = "StockFinancial"
        verbose_name_plural = "Stock Financials"
        db_table = "Stock_Financial"
        unique_together = ("statement", "fiscal_date", "period", "stock")
