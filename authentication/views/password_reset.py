from django.utils import timezone
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView

from authentication.models import EmailVerification
from authentication.serializers import PasswordResetSerializer
from authentication.tokens import hash_token
from core.response.response import error_response, success_response


class PasswordResetView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if not serializer.is_valid():
            return error_response(
                message="Invalid request",
                errors=serializer.errors,
                status=400,
            )

        token_hash = hash_token(serializer.validated_data["token"])
        new_password = serializer.validated_data["new_password"]

        try:
            verification = EmailVerification.objects.select_related("user").get(
                token_hash=token_hash,
                purpose="password_reset",
                is_used=False,
            )
        except EmailVerification.DoesNotExist:
            return error_response(
                message="Invalid or already used token",
                errors={"token": ["Invalid reset token"]},
                status=400,
            )

        if verification.expires_at < timezone.now():
            return error_response(
                message="Token has expired",
                errors={"token": ["Reset token expired"]},
                status=400,
            )

        user = verification.user
        user.set_password(new_password)
        user.save(update_fields=["password"])

        verification.is_used = True
        verification.used_at = timezone.now()
        verification.save(update_fields=["is_used", "used_at"])

        # Invalidate existing API tokens after password reset
        Token.objects.filter(user=user).delete()

        return success_response(
            data=None,
            message="Password reset successfully",
        )
