from django.conf import settings
from rest_framework.views import APIView

from authentication.emails import send_verification_email
from authentication.serializers import EmailResendSerializer
from authentication.services import create_verification_token
from core.response.response import error_response, success_response
from user.models import User


class ResendEmailView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = EmailResendSerializer(data=request.data)
        if not serializer.is_valid():
            return error_response(
                message="Invalid request",
                errors=serializer.errors,
                status=400,
            )

        email = serializer.validated_data["email"]

        # Same response always (no email enumeration)
        generic = success_response(
            data=None,
            message="If an account exists and is unverified, a verification email was sent.",
        )

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return generic

        if user.is_active:
            return generic

        raw_token = create_verification_token(user, purpose="signup", hours=24)
        send_verification_email(user, raw_token)

        data = None
        if settings.DEBUG:
            data = {"verification_token": raw_token}

        return success_response(
            data=data,
            message="If an account exists and is unverified, a verification email was sent.",
        )
