import structlog
from django.core.exceptions import ValidationError

logger = structlog.getLogger("django.server")


class SmallcaseResponseHandler:
    @staticmethod
    def handle_response(response):
        if 400 <= response.status_code < 500:
            sanitized_error = ",".join(response.json()["errors"]).strip(",")
            logger.error("Error Response ", response.json())
            raise ValidationError("API Error - " + sanitized_error, code=400)

        elif 500 <= response.status_code < 600:
            logger.error(response.json()["data"])
            raise ValidationError("Failed to get the Data", code=500)
