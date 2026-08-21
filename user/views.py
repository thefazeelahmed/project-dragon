from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ReadOnlyModelViewSet

from user.models import User
from user.serializer import UserSerializer


class UserViewSet(ReadOnlyModelViewSet):
    """Auth user endpoint — prefer /api/user-profiles/ for app identity."""

    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(pk=self.request.user.pk)
