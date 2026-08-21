from rest_framework.response import Response
from rest_framework.views import APIView

from core.response.response import success_response
from user.serializer import UserSerializer


class SignupView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            return success_response(
                data=UserSerializer(user).data,
                message="User signed up successfully",
                status=201,
            )

        return Response(
            {
                "success": False,
                "message": "Invalid credentials",
                "data": None,
                "errors": serializer.errors,
            },
            status=400,
        )
