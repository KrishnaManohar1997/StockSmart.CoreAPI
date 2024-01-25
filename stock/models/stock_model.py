import statistics
from django.db import models

from common.models import BaseStockModel

ALLOWED_RATIOS_FIELDS = [
    "52wHigh",
    "52wLow",
    "3mAvgVol",
    "12mVol",
    "4wpct",
    "52wpct",
    "pe",
    "pb",
    "divYield",
    "marketCap",
    "marketCapLabel",
    "beta",
]


def get_allowed_ratios_fields():
    return ALLOWED_RATIOS_FIELDS


def default_ratios_dict():
    return dict.fromkeys(ALLOWED_RATIOS_FIELDS, None)


class Stock(BaseStockModel):
    industry = models.CharField(max_length=64, blank=True, null=True)
    sector = models.CharField(max_length=64, blank=True, null=True)
    ratios = models.JSONField(default=default_ratios_dict, blank=False, null=False)
    ltp = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    prev_ltp = models.DecimalField(
        max_digits=8, decimal_places=2, blank=True, null=True
    )
    high = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    low = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    details = models.JSONField(default=None, blank=True, null=True)
    statistics = models.JSONField(default=None, blank=True, null=True)

    class Meta:
        verbose_name = "Stock"
        verbose_name_plural = "Stocks"
        db_table = "Stock"
