from django.db import IntegrityError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler


def api_exception_handler(exc: Exception, context):
    response = exception_handler(exc, context)

    if isinstance(exc, IntegrityError) and not response:
        response = Response({"message": exc.__str__()}, status=status.HTTP_400_BAD_REQUEST)

    return response
