from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated

from core.response.base_model_viewset import BaseModelViewSet
from tasks.models import Task
from tasks.serializer import TaskSerializer


class TaskViewSet(BaseModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    filterset_fields = ["project", "completed"]
    search_fields = ["title", "description"]
    ordering_fields = ["title", "created_at", "updated_at", "completed"]
    ordering = ["-created_at"]

    def get_queryset(self):
        return (
            Task.objects.filter(author=self.request.user)
            .select_related(
                "author",
                "project",
                "project__organization",
                "project__author",
            )
            .prefetch_related(
                "task_attachments",
                "task_attachments__attachment",
            )
        )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
