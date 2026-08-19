from attachments.models import Attachment
from attachments.serializers import AttachmentSerializer
from task_attachments.models import TaskAttachment
from rest_framework import serializers

class TaskAttachmentSerializer(serializers.ModelSerializer):
    attachment = AttachmentSerializer(read_only=True)
    attachment_id = serializers.PrimaryKeyRelatedField(
        source="attachment",
        queryset=Attachment.objects.all(),
        write_only=True
    )
    class Meta:
        model = TaskAttachment
        fields = '__all__'