from rest_framework import serializers

from organizations.models import Organization
from organizations.serializer import OrganizationSerializer
from user.serializer import UserSerializer
from .models import Project


class ProjectSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    organization = OrganizationSerializer(read_only=True)
    organization_id = serializers.PrimaryKeyRelatedField(
        source="organization",
        queryset=Organization.objects.all(),
        write_only=True,
    )

    class Meta:
        model = Project
        fields = [
            "id",
            "name",
            "description",
            "organization",
            "organization_id",
            "author",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["author", "created_at", "updated_at"]

    def validate_organization_id(self, organization):
        request = self.context.get("request")
        if request and request.user and request.user.is_authenticated:
            if organization.author_id != request.user.id:
                raise serializers.ValidationError(
                    "You can only create projects in your own organizations."
                )
        return organization
