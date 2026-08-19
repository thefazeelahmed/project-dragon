from django.urls import path

from organizations.views import OrganizationDetailView, OrganizationListCreateView


urlpatterns = [
    path("organizations/", OrganizationListCreateView.as_view()),
    path("organizations/<int:pk>/", OrganizationDetailView.as_view()),
]

