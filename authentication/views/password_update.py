from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from authentication.serializers import PasswordUpdateSerializer
from core.response.response import error_response, success_response


class PasswordUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PasswordUpdateSerializer(
            data=request.data,
            context={"request": request},
        )
        if not serializer.is_valid():
            return error_response(
                message="Password update failed",
                errors=serializer.errors,
                status=400,
            )

        user = request.user
        user.set_password(serializer.validated_data["new_password"])
        user.save(update_fields=["password"])

        return success_response(
            data=None,
            message="Password updated successfully",
        )
