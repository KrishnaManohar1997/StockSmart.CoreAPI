from django.core.management.base import BaseCommand

from smallcase.services.smallcase_service import SmallcaseService
from smallcase.models import Smallcase

import datetime


class Command(BaseCommand):
    help = "Load Smallcases"

    def __create_dummy_smallcases(self):
        dummy_smallcases = [
            {
                "symbol": "JUMBO_001",
                "name": "Captial Mind Momentum",
                "last_news_fetched_at": datetime.datetime(
                    2021, 9, 15, 12, 1, 47, 233709
                ),
                "latest_pub_news_date": datetime.datetime(
                    2021, 7, 27, 12, 1, 47, 229637
                ),
                "logo_url": "https://assets.smallcase.com/images/smallcases/160/SCET_0013.png",
                "price_52_week_high": 83.26,
                "price_52_week_low": 34.65,
                "publisher_name": "Windmill Capital",
                "description": "For long-term investors, dividend returns are very important as they are an additional income that is earned over and above the capital gains earned by holding onto the stock.",
                "last_rebalanced": datetime.datetime(2021, 6, 25, 0, 0),
                "risk_label": "Low Volatility",
                "risk_percentage": 2.2065972943429473,
                "minimum_investment": "15262.00",
                "constituents": [
                    {
                        "shares": 0.016923590466152962,
                        "ticker": "ATGL",
                        "weight": 0.5,
                        "stockName": "Adani Total Gas Ltd",
                        "industry": "Oil Marketing & Distribution",
                    },
                    {
                        "shares": 0.1664922952890185,
                        "ticker": "ONGC",
                        "weight": 0.5,
                        "stockName": "Oil and Natural Gas Corporation Ltd",
                        "industry": "Exploration & Production",
                    },
                ],
                "returns": {
                    "daily": 0.01460891649404411,
                    "weekly": 0.0006402311624103679,
                    "yearly": 1.0278150602964902,
                    "monthly": 0.12430960880424688,
                    "fiveYear": -0.26310975078428567,
                    "quarterly": -0.006213745689898394,
                    "threeYear": -0.26310975078428567,
                    "halfyearly": 0.12815879679945505,
                    "sinceLaunch": 0,
                    "sinceInception": -0.18876989052387338,
                },
                "cagr": 91.73045436971638,
                "index_value": 88.37335473202774,
            },
            {
                "symbol": "BRAND_0003",
                "name": "Brand Value",
                "last_news_fetched_at": datetime.datetime(
                    2021, 9, 15, 12, 1, 47, 233709
                ),
                "latest_pub_news_date": datetime.datetime(
                    2021, 7, 27, 12, 1, 47, 229637
                ),
                "logo_url": "https://assets.smallcase.com/images/smallcases/160/SCMO_0014.png",
                "price_52_week_high": 83.26,
                "price_52_week_low": 34.65,
                "publisher_name": "ICICI ",
                "description": "All Weather Investing is a popular strategy that ensures your investments do well in good as well as bad times. This is a long-term investment strategy that you can use to build wealth over the years to come.",
                "last_rebalanced": datetime.datetime(2021, 6, 25, 0, 0),
                "risk_label": "Medium Volatility",
                "risk_percentage": 2.2065972943429473,
                "minimum_investment": "8895.00",
                "constituents": [
                    {
                        "shares": 0.016923590466152962,
                        "ticker": "ATGL",
                        "weight": 0.25,
                        "stockName": "Adani Total Gas Ltd",
                        "industry": "Oil Marketing & Distribution",
                    },
                    {
                        "shares": 0.016923590466152962,
                        "ticker": "RELIANCE",
                        "weight": 0.25,
                        "stockName": "Reliance Industried Limited",
                        "industry": "Integrated Oil & Gas",
                    },
                    {
                        "shares": 0.1664922952890185,
                        "ticker": "ONGC",
                        "weight": 0.5,
                        "stockName": "Oil and Natural Gas Corporation Ltd",
                        "industry": "Exploration & Production",
                    },
                ],
                "returns": {
                    "daily": 0.01460891649404411,
                    "weekly": 0.0006402311624103679,
                    "yearly": 1.0278150602964902,
                    "monthly": 0.12430960880424688,
                    "fiveYear": -0.26310975078428567,
                    "quarterly": -0.006213745689898394,
                    "threeYear": -0.26310975078428567,
                    "halfyearly": 0.12815879679945505,
                    "sinceLaunch": 0,
                    "sinceInception": -0.18876989052387338,
                },
                "cagr": 51.73045436971638,
                "index_value": 41.37335473202774,
            },
            {
                "symbol": "BISECT_0021",
                "name": "Sector Hits",
                "last_news_fetched_at": datetime.datetime(
                    2021, 9, 15, 12, 1, 47, 233709
                ),
                "latest_pub_news_date": datetime.datetime(
                    2021, 7, 27, 12, 1, 47, 229637
                ),
                "logo_url": "https://assets.smallcase.com/images/smallcases/160/SCET_0014.png",
                "price_52_week_high": 83.26,
                "price_52_week_low": 34.65,
                "publisher_name": "Windmill Capital",
                "description": "An effective diversification strategy will require buying a wide variety of investments. International equity has comparatively lower correlation with Indian equity, thereby offering good diversification benefits.",
                "last_rebalanced": datetime.datetime(2021, 6, 25, 0, 0),
                "risk_label": "Medium Volatility",
                "risk_percentage": 2.2065972943429473,
                "minimum_investment": "16788.00",
                "constituents": [
                    {
                        "shares": 0.016923590466152962,
                        "ticker": "ATGL",
                        "weight": 0.25,
                        "stockName": "Adani Total Gas Ltd",
                        "industry": "Oil Marketing & Distribution",
                    },
                    {
                        "shares": 0.016923590466152962,
                        "ticker": "RELIANCE",
                        "weight": 0.25,
                        "stockName": "Reliance Industried Limited",
                        "industry": "Integrated Oil & Gas",
                    },
                    {
                        "shares": 0.1664922952890185,
                        "ticker": "ONGC",
                        "weight": 0.5,
                        "stockName": "Oil and Natural Gas Corporation Ltd",
                        "industry": "Exploration & Production",
                    },
                ],
                "returns": {
                    "daily": 0.15775790988,
                    "weekly": 0.0046789,
                    "yearly": 1.0278150602964902,
                    "monthly": 0.12430960880424688,
                    "fiveYear": -0.26310975078428567,
                    "quarterly": -0.006213745689898394,
                    "threeYear": -0.26310975078428567,
                    "halfyearly": 0.12815879679945505,
                    "sinceLaunch": 0,
                    "sinceInception": -0.18876989052387338,
                },
                "cagr": 123.73045436971638,
                "index_value": 152.37335473202774,
            },
        ]
        Smallcase.objects.bulk_create(
            [Smallcase(**smallcase) for smallcase in dummy_smallcases]
        )

    def handle(self, *args, **options):
        # Fetches all Smallcases and writes them to db
        SmallcaseService().load_db_with_smallcase_data()
