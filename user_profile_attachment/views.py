from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from user_profile_attachment.models import UserProfileAttachment
from user_profile_attachment.serializers import UserProfileAttachmentSerializer


class UserProfileAttachmentViewSet(ModelViewSet):
    serializer_class = UserProfileAttachmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            UserProfileAttachment.objects.filter(
                user_profile__user=self.request.user
            ).select_related("user_profile", "attachment")
        )

    def perform_create(self, serializer):
        serializer.save(user_profile=self.request.user.profile)
