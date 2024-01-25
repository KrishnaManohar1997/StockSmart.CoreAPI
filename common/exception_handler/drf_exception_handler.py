from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the our custom fields to the response.
    if response is not None:
        # Appends default result key with value False
        # As this state is always an Exception
        response.data["result"] = False
        # Update the Detail key as Message
        if "detail" in response.data:
            response.data["message"] = response.data.pop("detail")

    return response
