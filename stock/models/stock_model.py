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
    last_traded_at_price = models.DecimalField(max_digits=5, decimal_places=2)
    category = models.CharField(
        max_length=24,
        choices=StockCategory.choices(),
        default=StockCategory.FINANCIAL.value,
    )
    type = models.CharField(
        max_length=16,
        choices=SecurityType.choices(),
        default=SecurityType.EQUITY.value,
    )

    class Meta:
        db_table = "Stock"
        managed = True
        verbose_name = "Stock"
        verbose_name_plural = "Stocks"
