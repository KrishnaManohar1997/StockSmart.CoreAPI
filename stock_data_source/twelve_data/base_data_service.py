from django.conf import settings


class BaseDataService:
    API_KEY = settings.TWELVE_DATA_API_KEY
    BASE_URL = "https://api.twelvedata.com"
    DECIMAL_POINTS = 2
