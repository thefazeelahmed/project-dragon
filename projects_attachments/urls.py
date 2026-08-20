from django.urls import path, include
from rest_framework.routers import DefaultRouter
from projects_attachments.views import ProjectAttachmentView

router = DefaultRouter()
router.register(r'projects-attachments', ProjectAttachmentView, basename='projects-attachments')

urlpatterns = router.urls