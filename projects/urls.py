from django.urls import path
from .views import ProjectListCreateView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"projects", ProjectListCreateView, basename="projects")

urlpatterns = router.urls
