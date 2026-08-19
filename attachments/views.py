from rest_framework.viewsets import ModelViewSet

from .models import Attachment
from .serializers import AttachmentSerializer


class AttachmentViewSet(ModelViewSet):
    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer