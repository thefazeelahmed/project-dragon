from rest_framework.viewsets import ModelViewSet

from user.models import User
from user.serializer import UserSerializer

class LoginView(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer