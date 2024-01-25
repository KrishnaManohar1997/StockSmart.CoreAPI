from django.db import models

from common.models import BaseStockModel


class Smallcase(BaseStockModel):
    class RiskLabel(models.TextChoices):
        HIGH_VOLATILITY = "High Volatility"
        MEDIUM_VOLATILITY = "Medium Volatility"
        LOW_VOLATILITY = "Low Volatility"

    publisher_name = models.CharField(max_length=64, null=False, blank=False)
    description = models.CharField(max_length=256, blank=False, null=False)
    last_rebalanced = models.DateTimeField(blank=False, null=False)
    risk_label = models.CharField(
        max_length=32, blank=False, null=False, choices=RiskLabel.choices
    )
    risk_percentage = models.FloatField(blank=False, null=False)
    minimum_investment = models.DecimalField(
        blank=False, null=False, default=0, max_digits=10, decimal_places=2
    )
    constituents = models.JSONField(default=list, blank=False, null=False)
    returns = models.JSONField(default=list, blank=False, null=False)
    cagr = models.FloatField(blank=False, null=False)
    index_value = models.FloatField(blank=False, null=False)
    price_52_week_high = models.DecimalField(
        blank=False, null=False, default=0, max_digits=10, decimal_places=2
    )
    price_52_week_low = models.DecimalField(
        blank=False, null=False, default=0, max_digits=10, decimal_places=2
    )

    class Meta:
        verbose_name = "Smallcase"
        verbose_name_plural = "Smallcases"
        db_table = "Smallcase"
