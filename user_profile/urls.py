from rest_framework.routers import DefaultRouter

from user_profile.views import UserProfileViewSet

router = DefaultRouter()
router.register("user-profiles", UserProfileViewSet, basename="user-profiles")

urlpatterns = router.urls
