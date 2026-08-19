from django.shortcuts import render
from rest_framework import viewsets
from team_members.models import TeamMember
from team_members.serializer import TeamMemberSerializer

# Create your views here.
class TeamMemberViewSet(viewsets.ModelViewSet):
    queryset = TeamMember.objects.all()
    serializer_class = TeamMemberSerializer