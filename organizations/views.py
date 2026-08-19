from django.shortcuts import render
from rest_framework.views import APIView, Response, status

from organizations.models import Organization
from organizations.serializer import OrganizationSerializer

# Create your views here.
class OrganizationListCreateView(APIView):
    def get(self, request):
        organizations = Organization.objects.all()
        serializer = OrganizationSerializer(organizations, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = OrganizationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

class OrganizationDetailView(APIView):
    def get(self, request, pk):
        organization = Organization.objects.get(id=pk)
        serializer = OrganizationSerializer(organization)
        return Response(serializer.data)
    
    def put(self, request, pk):
        organization = Organization.objects.get(id=pk)
        serializer = OrganizationSerializer(organization, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
    
    def delete(self, request, pk):
        organization = Organization.objects.get(id=pk)
        organization.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def patch(self, request, pk):
        organization = Organization.objects.get(id=pk)
        serializer = OrganizationSerializer(organization, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)