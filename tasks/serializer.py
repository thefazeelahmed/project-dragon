from rest_framework import serializers

from projects.serializers import ProjectSerializer
from task_attachments.models import TaskAttachment
from task_attachments.serializer import TaskAttachmentSerializer
from .models import Task


class TaskSerializer(serializers.ModelSerializer):

    project = ProjectSerializer(read_only=True)
    project_id = serializers.PrimaryKeyRelatedField(
        source="project",
        queryset=Task._meta.get_field("project").remote_field.model.objects.all(),
        write_only=True
    )

    
    task_attachments = TaskAttachmentSerializer(many=True,
        read_only=True)

    class Meta:
        model = Task
        fields = '__all__'