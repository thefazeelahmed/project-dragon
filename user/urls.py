from rest_framework.routers import DefaultRouter

from user.views import UserViewSet

router = DefaultRouter()
router.register("users", UserViewSet, basename="users")

urlpatterns = router.urls
