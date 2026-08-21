from rest_framework import serializers

from attachments.models import Attachment
from attachments.serializers import AttachmentSerializer
from user_profile_attachment.models import UserProfileAttachment


class UserProfileAttachmentSerializer(serializers.ModelSerializer):
    attachment = AttachmentSerializer(read_only=True)
    attachment_id = serializers.PrimaryKeyRelatedField(
        source="attachment",
        queryset=Attachment.objects.all(),
        write_only=True,
    )

    class Meta:
        model = UserProfileAttachment
        fields = [
            "id",
            "attachment",
            "attachment_id",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]
