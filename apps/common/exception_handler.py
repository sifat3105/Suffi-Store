from rest_framework.views import exception_handler
from rest_framework import status
from .response import custom_response

from rest_framework.views import exception_handler
from rest_framework import status
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework.exceptions import AuthenticationFailed
from .response import custom_response

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if isinstance(exc, (InvalidToken, TokenError, AuthenticationFailed)):
        message = "Invalid or expired token."

        if hasattr(exc, "args") and exc.args:
            detail = exc.args[0]
            if isinstance(detail, dict) and "messages" in detail:
                msg_list = detail.get("messages", [])
                if msg_list and isinstance(msg_list, list):
                    first_msg = msg_list[0].get("message")
                    if first_msg:
                        message = str(first_msg)

        return custom_response(
            status="error",
            status_code=status.HTTP_401_UNAUTHORIZED,
            message=message,
            data=None
        )
    if response is not None:
        if response.status_code == status.HTTP_401_UNAUTHORIZED:
            return custom_response(
                status="error",
                status_code=status.HTTP_401_UNAUTHORIZED,
                message="Authentication credentials were not provided.",
                data=None
            )
        elif response.status_code == status.HTTP_403_FORBIDDEN:
            return custom_response(
                status="error",
                status_code=status.HTTP_403_FORBIDDEN,
                message="You do not have permission to perform this action.",
                data=None
            )
        elif response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED:
            return custom_response(
                status="error",
                status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                message=f"Method {context['request'].method} not allowed on this endpoint.",
                data=None
            )

    return response
