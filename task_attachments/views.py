from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from task_attachments.models import TaskAttachment
from task_attachments.serializer import TaskAttachmentSerializer


class TaskAttachmentViewSet(ModelViewSet):
    serializer_class = TaskAttachmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            TaskAttachment.objects.filter(task__author=self.request.user)
            .select_related("task", "task__author", "attachment")
        )
