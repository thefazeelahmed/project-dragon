import datetime
from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        response.data['status_code'] = response.status_code
        response.data['message'] = response.data['detail']
        response.data['data'] = None
        response.data['errors'] = response.data['detail']
        response.data['success'] = False
        response.data['timestamp'] = datetime.now().isoformat()
        response.data['path'] = context['request'].path
        response.data['method'] = context['request'].method
        response.data['status'] = response.status_code
        response.data['traceback'] = response.data['detail']
    return response