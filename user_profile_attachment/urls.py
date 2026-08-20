from django.urls import path
from rest_framework.routers import DefaultRouter

from user_profile_attachment.views import UserProfileAttachmentView

router = DefaultRouter()
router.register(r'user-profile-attachment', UserProfileAttachmentView, basename='user-profile-attachment')

urlpatterns = router.urls