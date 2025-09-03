from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        if 'detail' in response.data:
            response.data['message'] = response.data['detail']
            del response.data['detail']

        response.data['status'] = 'error'

    return response

def error_response(message: str, code: int = status.HTTP_403_FORBIDDEN):
    return Response({
        "status": "error",
        "message": message
    }, status=code)

