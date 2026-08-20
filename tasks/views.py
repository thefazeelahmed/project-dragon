from rest_framework import viewsets
from rest_framework.views import APIView, Response

from core.response.base_model_viewset import BaseModelViewSet
from tasks.models import Task
from tasks.serializer import TaskSerializer

# Create your views here.

class TaskViewSet(BaseModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer