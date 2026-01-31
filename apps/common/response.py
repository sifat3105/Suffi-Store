from rest_framework.response import Response

def custom_response(status: str, status_code: int, message: str, data=None):
    return Response({
        "status": status,
        "status_code": status_code,
        "message": message,
        "data": data
    }, status=status_code)
