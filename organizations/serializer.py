from rest_framework import serializers

from user.serializer import UserSerializer
from .models import Organization


class OrganizationSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Organization
        fields = [
            "id",
            "name",
            "description",
            "author",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["author", "created_at", "updated_at"]
