from projects_attachments.models import ProjectAttachment
from projects_attachments.serializer import ProjectAttachmentSerializer
from rest_framework import viewsets

class ProjectAttachmentView(viewsets.ModelViewSet):
    queryset = ProjectAttachment.objects.all()
    serializer_class = ProjectAttachmentSerializer