from django.db import models

from common.constants import SecurityType, StockCategory
from common.models import BaseModel


class Stock(BaseModel):
    name = models.CharField(
        max_length=128, blank=False, null=False, db_index=True, unique=True
    )
    symbol = models.CharField(
        max_length=16, blank=False, null=False, db_index=True, unique=True
    )
    last_traded_at_price = models.CharField(max_length=64, blank=False, null=False)
    category = models.CharField(
        max_length=16,
        choices=StockCategory.choices(),
        default=StockCategory.FINANCIAL.value,
    )
    type = models.CharField(
        max_length=16,
        choices=SecurityType.choices(),
        default=StockCategory.EQUITY.value,
    )

    class Meta:
        db_table = "Stock"
        managed = True
        verbose_name = "Stock"
        verbose_name_plural = "Stocks"
