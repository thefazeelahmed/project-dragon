from rest_framework import serializers

from projects.models import Project
from projects.serializers import ProjectSerializer
from task_attachments.serializer import TaskAttachmentSerializer
from user.serializer import UserSerializer
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    project = ProjectSerializer(read_only=True)
    project_id = serializers.PrimaryKeyRelatedField(
        source="project",
        queryset=Project.objects.all(),
        write_only=True,
    )
    task_attachments = TaskAttachmentSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "project",
            "project_id",
            "author",
            "completed",
            "task_attachments",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["author", "created_at", "updated_at"]

    def validate_project_id(self, project):
        request = self.context.get("request")
        if request and request.user and request.user.is_authenticated:
            if project.author_id != request.user.id:
                raise serializers.ValidationError(
                    "You can only create tasks in your own projects."
                )
        return project
