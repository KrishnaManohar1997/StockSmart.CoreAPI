import structlog
from django.core.exceptions import ValidationError

from common.helper import APIResponseHandler

logger = structlog.getLogger("django.server")


class NSEResponseHandler(APIResponseHandler):
    @staticmethod
    def handle_response(response):
        if 400 <= response.status_code < 500:
            logger.error("Error Response ", response.text)
            raise ValidationError("NSE API Error", code=400)

        elif 500 <= response.status_code < 600:
            logger.error("Error Response ", response.text)
            raise ValidationError("Failed to get the Data NSE API", code=500)
