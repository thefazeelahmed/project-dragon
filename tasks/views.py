from rest_framework import viewsets
from rest_framework.views import APIView, Response

from tasks.models import Task
from tasks.serializer import TaskSerializer

# Create your views here.

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer