from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.views import APIView

from core.response.response import success_response
from user.serializer import UserSerializer


class LoginView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response(
                {
                    "success": False,
                    "message": "Email and password are required",
                    "data": None,
                    "errors": {"detail": "Missing credentials"},
                },
                status=400,
            )

        # USERNAME_FIELD = "email", so authenticate(email=...) works
        user = authenticate(request=request, email=email, password=password)

        if user is not None:
            return success_response(
                data=UserSerializer(user).data,
                message="User logged in successfully",
            )

        return Response(
            {
                "success": False,
                "message": "Invalid credentials",
                "data": None,
                "errors": {"detail": "Invalid email or password"},
            },
            status=401,
        )
