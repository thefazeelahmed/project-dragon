from django.urls import path

from authentication.views.login_view import LoginView
from authentication.views.signup_view import SignupView




urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('signup/', SignupView.as_view(), name='signup'),
]