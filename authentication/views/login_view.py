from rest_framework.authtoken.models import Token
from rest_framework.views import APIView

from authentication.serializers import LoginSerializer
from core.response.response import error_response, success_response
from user.serializer import UserSerializer


class LoginView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={"request": request})
        if not serializer.is_valid():
            return error_response(
                message="Login failed",
                errors=serializer.errors,
                status=401,
            )

        user = serializer.validated_data["user"]
        token, _ = Token.objects.get_or_create(user=user)

        return success_response(
            data={
                "user": UserSerializer(user).data,
                "token": token.key,
            },
            message="User logged in successfully",
        )
