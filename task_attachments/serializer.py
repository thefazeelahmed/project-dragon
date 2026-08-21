from rest_framework import serializers

from attachments.models import Attachment
from attachments.serializers import AttachmentSerializer
from tasks.models import Task
from task_attachments.models import TaskAttachment


class TaskAttachmentSerializer(serializers.ModelSerializer):
    attachment = AttachmentSerializer(read_only=True)
    attachment_id = serializers.PrimaryKeyRelatedField(
        source="attachment",
        queryset=Attachment.objects.all(),
        write_only=True,
    )
    task_id = serializers.PrimaryKeyRelatedField(
        source="task",
        queryset=Task.objects.all(),
        write_only=True,
    )

    class Meta:
        model = TaskAttachment
        fields = [
            "id",
            "task",
            "task_id",
            "attachment",
            "attachment_id",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["task", "created_at", "updated_at"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get("request")
        if request and request.user and request.user.is_authenticated:
            self.fields["task_id"].queryset = Task.objects.filter(author=request.user)

    def validate_task_id(self, task):
        request = self.context.get("request")
        if request and request.user and request.user.is_authenticated:
            if task.author_id != request.user.id:
                raise serializers.ValidationError(
                    "You can only attach files to your own tasks."
                )
        return task
