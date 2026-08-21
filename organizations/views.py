from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from organizations.models import Organization
from organizations.serializer import OrganizationSerializer


class OrganizationViewSet(ModelViewSet):
    serializer_class = OrganizationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # A user can have multiple orgs — list only theirs
        return Organization.objects.filter(
            author=self.request.user
        ).select_related("author")

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
