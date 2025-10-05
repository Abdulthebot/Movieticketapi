from rest_framework.views import exception_handler
from rest_framework.response import Response

# A custom exception handler ensures all API error responses follow a consistent format[cite: 255].
def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        custom_response_data = {
            'status_code': response.status_code,
            'error': {
                'type': exc.__class__.__name__,
                'detail': response.data
            }
        }
        response.data = custom_response_data
    
    return response