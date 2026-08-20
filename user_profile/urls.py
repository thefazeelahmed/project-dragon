from django.urls import path
from rest_framework.routers import DefaultRouter

from user_profile.views import UserProfileView

router = DefaultRouter()
router.register(r'user-profile', UserProfileView, basename='user-profile')

urlpatterns = router.urls