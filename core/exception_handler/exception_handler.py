from rest_framework.response import Response
from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        detail = response.data.get("detail", response.data)
        return Response(
            {
                "success": False,
                "message": detail if isinstance(detail, str) else "Error",
                "data": None,
                "errors": response.data,
            },
            status=response.status_code,
        )

    return Response(
        {
            "success": False,
            "message": "Internal Server Error",
            "data": None,
            "errors": {"detail": str(exc)},
        },
        status=500,
    )