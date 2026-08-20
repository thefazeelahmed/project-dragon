from rest_framework import serializers
from projects_attachments.models import ProjectAttachment

class ProjectAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectAttachment
        fields = '__all__'