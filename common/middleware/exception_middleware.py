from django.core.exceptions import ValidationError
from django.http import JsonResponse


class ErrorHandlerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        # Validation Errors will be taken care at Middleware Level
        if type(exception) is ValidationError:
            try:
                exception_code = int(exception.code)
            except (ValueError, AttributeError, TypeError):
                exception_code = 400
            return JsonResponse(
                {
                    "result": False,
                    "message": exception.message,
                },
                status=exception_code,
            )
