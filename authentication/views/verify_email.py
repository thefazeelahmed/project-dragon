from django.utils import timezone
from rest_framework.views import APIView

from authentication.models import EmailVerification
from authentication.serializers import EmailVerifySerializer
from authentication.tokens import hash_token
from core.response.response import error_response, success_response


class VerifyEmailView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = EmailVerifySerializer(data=request.data)
        if not serializer.is_valid():
            return error_response(
                message="Invalid request",
                errors=serializer.errors,
                status=400,
            )

        token_hash = hash_token(serializer.validated_data["token"])

        try:
            verification = EmailVerification.objects.select_related("user").get(
                token_hash=token_hash,
                purpose="signup",
                is_used=False,
            )
        except EmailVerification.DoesNotExist:
            return error_response(
                message="Invalid or already used token",
                errors={"token": ["Invalid verification token"]},
                status=400,
            )

        if verification.expires_at < timezone.now():
            return error_response(
                message="Token has expired",
                errors={"token": ["Verification token expired"]},
                status=400,
            )

        user = verification.user
        user.is_active = True
        user.save(update_fields=["is_active"])

        verification.is_used = True
        verification.used_at = timezone.now()
        verification.save(update_fields=["is_used", "used_at"])

        return success_response(
            data={"email": user.email, "is_active": user.is_active},
            message="Email verified successfully",
        )
