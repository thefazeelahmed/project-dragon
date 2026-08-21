from django.urls import path

from authentication.views.login_view import LoginView
from authentication.views.password_forgot import PasswordForgotView
from authentication.views.password_reset import PasswordResetView
from authentication.views.password_update import PasswordUpdateView
from authentication.views.resend_email import ResendEmailView
from authentication.views.signup_view import SignupView
from authentication.views.verify_email import VerifyEmailView

urlpatterns = [
    path("signup/", SignupView.as_view(), name="auth-signup"),
    path("login/", LoginView.as_view(), name="auth-login"),
    path("email/verify/", VerifyEmailView.as_view(), name="auth-email-verify"),
    path("email/resend/", ResendEmailView.as_view(), name="auth-email-resend"),
    path("password/update/", PasswordUpdateView.as_view(), name="auth-password-update"),
    path("password/forgot/", PasswordForgotView.as_view(), name="auth-password-forgot"),
    path("password/reset/", PasswordResetView.as_view(), name="auth-password-reset"),
]
