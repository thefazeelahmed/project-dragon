from rest_framework import serializers

from organizations.serializer import OrganizationSerializer
from .models import Project


class ProjectSerializer(serializers.ModelSerializer):
    organization = OrganizationSerializer(read_only=True)
    organization_id = serializers.PrimaryKeyRelatedField(
        source="organization",
        queryset=Project._meta.get_field("organization").remote_field.model.objects.all(),
        write_only=True
    )

    class Meta:
        model = Project
        fields = [
            "id",
            "name",
            "description",
            "organization",
            "organization_id",
            "created_at",
            "updated_at",
        ]