from django.shortcuts import render

from user_profile_attachment.models import UserProfileAttachment
from user_profile_attachment.serliazers import UserProfileAttachmentSerializer

# Create your views here.
class UserProfileAttachmentView(ModelViewSet):
    queryset = UserProfileAttachment.objects.all()
    serializer_class = UserProfileAttachmentSerializer