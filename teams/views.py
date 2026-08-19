from django.shortcuts import render
from rest_framework import viewsets
from teams.models import Team
from teams.serializer import TeamSerializer

# Create your views here.
class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer