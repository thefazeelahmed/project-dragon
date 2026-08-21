from rest_framework.authtoken.models import Token
from rest_framework.views import APIView

from authentication.serializers import LoginSerializer
from core.response.response import error_response, success_response
from user_profile.models import UserProfile
from user_profile.serializer import UserProfileSerializer


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

        profile, _ = UserProfile.objects.get_or_create(user=user, defaults={"bio": ""})
        profile = (
            UserProfile.objects.filter(pk=profile.pk)
            .select_related("user")
            .prefetch_related(
                "profile_attachments",
                "profile_attachments__attachment",
            )
            .get()
        )

        return success_response(
            data={
                "profile": UserProfileSerializer(profile).data,
                "token": token.key,
            },
            message="User logged in successfully",
        )
