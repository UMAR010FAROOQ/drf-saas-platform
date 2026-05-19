import logging

from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError


logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):

    response = drf_exception_handler(exc, context)

    if response is not None:

        data = response.data

        if isinstance(exc, ValidationError):
            message = "Validation failed"
        else:
            message = data.get("detail", "Request failed")

        return Response({
            "success": False,
            "message": message,
            "errors": data
        }, status=response.status_code)

    logger.exception("Unhandled exception occurred", exc_info=exc)

    return Response({
        "success": False,
        "message": "Internal server error",
        "error_code": "server_error"
    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)