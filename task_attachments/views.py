from rest_framework import viewsets
from task_attachments.models import TaskAttachment
from task_attachments.serializer import TaskAttachmentSerializer

# Create your views here.
class TaskAttachmentViewSet(viewsets.ModelViewSet):
    queryset = TaskAttachment.objects.all()
    serializer_class = TaskAttachmentSerializer