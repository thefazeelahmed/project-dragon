from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from user_profile.models import UserProfile
from user_profile.serializer import UserProfileSerializer


class UserProfileViewSet(ModelViewSet):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "patch", "head", "options"]

    def get_queryset(self):
        return (
            UserProfile.objects.filter(user=self.request.user)
            .select_related("user")
            .prefetch_related(
                "profile_attachments",
                "profile_attachments__attachment",
            )
        )
