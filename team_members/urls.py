from rest_framework.routers import DefaultRouter

from team_members.views import TeamMemberViewSet

router = DefaultRouter()
router.register("team-members", TeamMemberViewSet)

urlpatterns = router.urls