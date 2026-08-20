from rest_framework import serializers
from attachments.models import Attachment
from attachments.serializers import AttachmentSerializer
from projects_attachments.models import ProjectAttachment

class ProjectAttachmentSerializer(serializers.ModelSerializer):
    attachment = AttachmentSerializer(read_only=True)
    attachment_id = serializers.PrimaryKeyRelatedField(
        source="attachment",
        queryset=Attachment.objects.all(),
        write_only=True
    )
    class Meta:
        model = ProjectAttachment
        fields = '__all__'