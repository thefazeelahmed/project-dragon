import datetime
from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        response.data['status_code'] = response.status_code
        response.data['message'] = response.data['detail']
        response.data['data'] = None
        response.data['success'] = False
        return response
    response.data['status_code'] = 500
    response.data['message'] = "Internal Server Error"
    response.data['data'] = None
    response.data['success'] = False
    return response


