from django.urls import path
from rest_framework.routers import DefaultRouter

from user.views import UserView

router = DefaultRouter()
router.register(r'user', UserView, basename='user')

urlpatterns = router.urls