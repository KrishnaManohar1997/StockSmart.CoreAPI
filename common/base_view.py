from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from common.auth.stocksmart_token_authentication import PublicAuthentication
from common.helper.readable_serializer_error_translator import (
    translate_serializer_errors,
)


class BaseView(APIView):
    def success_response(self, message):
        return Response(
            {"result": True, "message": message},
            status=status.HTTP_200_OK,
        )

    def data_response(self, message, data):
        return Response(
            {"result": True, "message": message, "data": data},
            status=status.HTTP_200_OK,
        )

    def resource_created_response(self, resource, resource_id):
        return Response(
            {
                "result": True,
                "message": f"{resource} created successfully",
                "id": resource_id,
            },
            status=status.HTTP_201_CREATED,
        )

    def resource_created_data_response(self, resource, resource_id, data):
        return Response(
            {
                "result": True,
                "message": f"{resource} created successfully",
                "id": resource_id,
                "data": data,
            },
            status=status.HTTP_201_CREATED,
        )

    def resource_updated_response(self, resource, resource_id):
        return Response(
            {
                "result": True,
                "message": f"{resource} with {resource_id} updated successfully",
            },
            status=status.HTTP_202_ACCEPTED,
        )

    def resource_deleted_response(self, message, resource_id=None):
        return Response(
            {"result": True, "message": message, "id": resource_id},
            status=status.HTTP_202_ACCEPTED,
        )

    def bad_request_response(self, message):
        # Handles Error Objects Internally by Converting them To String
        return Response(
            {"result": False, "message": str(message)},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def serializer_error_response(self, message: str, serializer_errors: dict):
        serializer_errors = translate_serializer_errors(serializer_errors)
        return self.bad_request_response("{}. {}".format(message, serializer_errors))

    def unauthorized_response(self, message="Unauthorized Access"):
        return Response(
            {"result": False, "message": message},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    def resource_forbidden_response(self, message="Forbidden Action"):
        return Response(
            {"result": False, "message": message},
            status=status.HTTP_403_FORBIDDEN,
        )

    def resource_not_found_response(self, resource, id=None):
        if id:
            message = f"{resource} - {id} doesn't exist "
        else:
            message = f"Requested {resource} doesn't exist "
        return Response(
            {"result": False, "message": message},
            status=status.HTTP_404_NOT_FOUND,
        )

    def paginated_response(self, paginator, message, data):
        return paginator.get_paginated_response(
            {"result": True, "message": message, "data": data}
        )

    def empty_paginated_response(self, message):
        # Can be used in places wherever the Empty paginated response
        # will be needed
        return Response(
            {
                "count": 0,
                "next": None,
                "previous": None,
                "results": {"result": True, "message": message, "data": []},
            }
        )

    class Meta:
        abstract = True


class PublicBaseView(BaseView):
    authentication_classes = [PublicAuthentication]
    permission_classes = []

    class Meta:
        abstract = True
