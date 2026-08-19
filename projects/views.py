# from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework import status
# from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet

from .models import Project
from .serializers import ProjectSerializer


# class ProjectListCreateView(ListCreateAPIView):

#     def get(self, request):
#         projects = Project.objects.all()
#         serializer = ProjectSerializer(projects, many=True)

#         return Response(serializer.data)

    #     def post(self, request):
#         serializer = ProjectSerializer(data=request.data)

#         if serializer.is_valid():
#             project = serializer.save()

#             return Response(
#                 ProjectSerializer(project).data,
#                 status=status.HTTP_201_CREATED
#             )

# class ProjectListCreateView(ListCreateAPIView):
#     queryset = Project.objects.all()
#     serializer_class = ProjectSerializer
#     filter_backends = [SearchFilter,
#         OrderingFilter,
#         DjangoFilterBackend,]
#     filterset_fields = ["organization"]

#     search_fields = [
#         "name",
#         "description",
#     ]

#     ordering_fields = [
#         "name",
#         "created_at",
#         "updated_at",
#     ]

#     ordering = ["-created_at"]


# class ProjectDetailView(APIView):

#     def get(self, request, pk):
#         try:
#             project = Project.objects.get(pk=pk)
#         except Project.DoesNotExist:
#             return Response(
#                 {"detail": "Project not found."},
#                 status=status.HTTP_404_NOT_FOUND
#             )

#         serializer = ProjectSerializer(project)

#         return Response(serializer.data)

#     def put(self, request, pk):
#         try:
#             project = Project.objects.get(pk=pk)
#         except Project.DoesNotExist:
#             return Response(
#                 {"detail": "Project not found."},
#                 status=status.HTTP_404_NOT_FOUND
#             )
#         serializer = ProjectSerializer(
#             project,
#             data=request.data
#         )

#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)

#         return Response(
#             serializer.errors,
#             status=status.HTTP_400_BAD_REQUEST
#         )

#     def patch(self, request, pk):
#         try:
#             project = Project.objects.get(pk=pk)
#         except Project.DoesNotExist:
#             return Response(
#                 {"detail": "Project not found."},
#                 status=status.HTTP_404_NOT_FOUND
#             )

#         serializer = ProjectSerializer(
#             project,
#             data=request.data,
#             partial=True
#         )

#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)

#         return Response(
#             serializer.errors,
#             status=status.HTTP_400_BAD_REQUEST
#         )

#     def delete(self, request, pk):
#         try:
#             project = Project.objects.get(pk=pk)
#         except Project.DoesNotExist:
#             return Response(
#                 {"detail": "Project not found."},
#                 status=status.HTTP_404_NOT_FOUND
#             )

#         project.delete()

#         return Response(
#             status=status.HTTP_204_NO_CONTENT
#         )

class ProjectListCreateView(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    filter_backends = [SearchFilter,
        OrderingFilter,
        DjangoFilterBackend,]
    filterset_fields = ["organization"]

    search_fields = [
        "name",
        "description",
    ]