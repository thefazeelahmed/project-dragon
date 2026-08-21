from rest_framework.routers import DefaultRouter

from user_profile_attachment.views import UserProfileAttachmentViewSet

router = DefaultRouter()
router.register(
    "user-profile-attachments",
    UserProfileAttachmentViewSet,
    basename="user-profile-attachments",
)

urlpatterns = router.urls
