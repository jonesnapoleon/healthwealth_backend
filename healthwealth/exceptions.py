from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.

    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    if response is not None:
        status_code = response.status_code

    code = exc.__class__.__name__
    detail = str(exc)
    response = Response(
        data={
            "code": code,
            "detail": detail,
        },
        status=status_code,
    )
    return response


class HealthWealthException(Exception):
    def __init__(self, detail=None, code=None, status_code=None):
        if code is None:
            code = "unknown_error"

        if status_code is None:
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

        self.detail = detail
        self.code = code
        self.status_code = status_code

    def as_response(self):
        return Response(
            {
                "code": self.code,
                "detail": self.detail,
            },
            status=self.status_code,
        )
