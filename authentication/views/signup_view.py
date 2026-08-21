from django.conf import settings
from rest_framework.views import APIView

from authentication.emails import send_verification_email
from authentication.serializers import SignupSerializer
from authentication.services import create_verification_token
from core.response.response import error_response, success_response
from user.serializer import UserSerializer


class SignupView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if not serializer.is_valid():
            return error_response(
                message="Signup failed",
                errors=serializer.errors,
                status=400,
            )

        user = serializer.save()
        raw_token = create_verification_token(user, purpose="signup", hours=24)
        send_verification_email(user, raw_token)

        payload = UserSerializer(user).data
        if settings.DEBUG:
            payload["verification_token"] = raw_token

        return success_response(
            data=payload,
            message="User signed up successfully. Please verify your email.",
            status=201,
        )
