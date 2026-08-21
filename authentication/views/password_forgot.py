from django.conf import settings
from rest_framework.views import APIView

from authentication.emails import send_password_reset_email
from authentication.serializers import PasswordForgotSerializer
from authentication.services import create_verification_token
from core.response.response import error_response, success_response
from user.models import User


class PasswordForgotView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = PasswordForgotSerializer(data=request.data)
        if not serializer.is_valid():
            return error_response(
                message="Invalid request",
                errors=serializer.errors,
                status=400,
            )

        email = serializer.validated_data["email"]
        generic = success_response(
            data=None,
            message="If an account exists, a password reset email was sent.",
        )

        try:
            user = User.objects.get(email=email, is_active=True)
        except User.DoesNotExist:
            return generic

        raw_token = create_verification_token(user, purpose="password_reset", hours=1)
        send_password_reset_email(user, raw_token)

        data = None
        if settings.DEBUG:
            data = {"reset_token": raw_token}

        return success_response(
            data=data,
            message="If an account exists, a password reset email was sent.",
        )
