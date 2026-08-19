from rest_framework.routers import DefaultRouter

from task_attachments.views import TaskAttachmentViewSet

router = DefaultRouter()
router.register("task-attachments", TaskAttachmentViewSet)

urlpatterns = router.urls