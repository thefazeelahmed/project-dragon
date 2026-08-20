from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from user_profile.models import UserProfile
from user_profile.serializer import UserProfileSerializer

# Create your views here.
class UserProfileView(ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer