"""
Auth logical API tests (business rules + mocked email side-effects).
"""

from unittest.mock import patch

from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from authentication.models import EmailVerification
from authentication.tokens import hash_token
from user.models import User
from user_profile.models import UserProfile


class AuthLogicAPITests(APITestCase):
    def setUp(self):
        self.signup_url = reverse("auth-signup")
        self.verify_url = reverse("auth-email-verify")
        self.login_url = reverse("auth-login")
        self.resend_url = reverse("auth-email-resend")
        self.forgot_url = reverse("auth-password-forgot")
        self.reset_url = reverse("auth-password-reset")
        self.update_url = reverse("auth-password-update")
        self.user_payload = {
            "name": "Fazeel",
            "email": "fazeel@example.com",
            "password": "secret12345",
        }

    def _signup(self, mock_send_email):
        response = self.client.post(self.signup_url, self.user_payload, format="json")
        raw_token = mock_send_email.call_args[0][1]
        return response, raw_token

    def _signup_and_verify(self, mock_send_email):
        _, raw_token = self._signup(mock_send_email)
        self.client.post(self.verify_url, {"token": raw_token}, format="json")
        return User.objects.get(email=self.user_payload["email"])

    # 1) Signup: inactive user + hashed token + email mocked
    @patch("authentication.views.signup_view.send_verification_email")
    def test_signup_creates_inactive_user_and_hashed_token(self, mock_send_email):
        response, raw_token = self._signup(mock_send_email)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data["success"])

        user = User.objects.get(email=self.user_payload["email"])
        self.assertFalse(user.is_active)

        mock_send_email.assert_called_once()
        verification = EmailVerification.objects.get(user=user, purpose="signup")
        self.assertNotEqual(verification.token_hash, raw_token)
        self.assertEqual(verification.token_hash, hash_token(raw_token))

    # 2) Signup creates UserProfile
    @patch("authentication.views.signup_view.send_verification_email")
    def test_signup_creates_user_profile(self, mock_send_email):
        response, _ = self._signup(mock_send_email)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(email=self.user_payload["email"])
        self.assertTrue(UserProfile.objects.filter(user=user).exists())
        self.assertEqual(response.data["data"]["user"]["email"], user.email)

    # 3) Verify activates user + token is one-time
    @patch("authentication.views.signup_view.send_verification_email")
    def test_verify_email_activates_user(self, mock_send_email):
        _, raw_token = self._signup(mock_send_email)

        response = self.client.post(
            self.verify_url, {"token": raw_token}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        user = User.objects.get(email=self.user_payload["email"])
        self.assertTrue(user.is_active)
        self.assertTrue(
            EmailVerification.objects.get(user=user, purpose="signup").is_used
        )

        again = self.client.post(
            self.verify_url, {"token": raw_token}, format="json"
        )
        self.assertEqual(again.status_code, status.HTTP_400_BAD_REQUEST)

    # 4) Login blocked before verify; after verify returns profile + token
    @patch("authentication.views.signup_view.send_verification_email")
    def test_login_requires_verified_email_and_returns_profile(
        self, mock_send_email
    ):
        _, raw_token = self._signup(mock_send_email)

        before = self.client.post(
            self.login_url,
            {
                "email": self.user_payload["email"],
                "password": self.user_payload["password"],
            },
            format="json",
        )
        self.assertEqual(before.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.post(self.verify_url, {"token": raw_token}, format="json")

        after = self.client.post(
            self.login_url,
            {
                "email": self.user_payload["email"],
                "password": self.user_payload["password"],
            },
            format="json",
        )
        self.assertEqual(after.status_code, status.HTTP_200_OK)
        self.assertIn("token", after.data["data"])
        self.assertIn("profile", after.data["data"])
        self.assertEqual(
            after.data["data"]["profile"]["user"]["email"],
            self.user_payload["email"],
        )

    # 5) Wrong password fails after verify
    @patch("authentication.views.signup_view.send_verification_email")
    def test_login_fails_with_wrong_password(self, mock_send_email):
        self._signup_and_verify(mock_send_email)

        response = self.client.post(
            self.login_url,
            {
                "email": self.user_payload["email"],
                "password": "wrong-password",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # 6) Resend verification email for unverified user
    @patch("authentication.views.resend_email.send_verification_email")
    @patch("authentication.views.signup_view.send_verification_email")
    def test_resend_verification_email(self, mock_signup_email, mock_resend_email):
        self._signup(mock_signup_email)

        response = self.client.post(
            self.resend_url,
            {"email": self.user_payload["email"]},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_resend_email.assert_called_once()

        user = User.objects.get(email=self.user_payload["email"])
        self.assertTrue(
            EmailVerification.objects.filter(
                user=user, purpose="signup", is_used=False
            ).exists()
        )

    # 7) Forgot + reset password, then login with new password
    @patch("authentication.views.password_forgot.send_password_reset_email")
    @patch("authentication.views.signup_view.send_verification_email")
    def test_forgot_and_reset_password_flow(
        self, mock_signup_email, mock_reset_email
    ):
        user = self._signup_and_verify(mock_signup_email)
        old_token, _ = Token.objects.get_or_create(user=user)

        forgot = self.client.post(
            self.forgot_url,
            {"email": self.user_payload["email"]},
            format="json",
        )
        self.assertEqual(forgot.status_code, status.HTTP_200_OK)
        mock_reset_email.assert_called_once()
        reset_token = mock_reset_email.call_args[0][1]

        reset = self.client.post(
            self.reset_url,
            {"token": reset_token, "new_password": "newsecret999"},
            format="json",
        )
        self.assertEqual(reset.status_code, status.HTTP_200_OK)
        self.assertFalse(Token.objects.filter(key=old_token.key).exists())

        login_old = self.client.post(
            self.login_url,
            {
                "email": self.user_payload["email"],
                "password": self.user_payload["password"],
            },
            format="json",
        )
        self.assertEqual(login_old.status_code, status.HTTP_401_UNAUTHORIZED)

        login_new = self.client.post(
            self.login_url,
            {
                "email": self.user_payload["email"],
                "password": "newsecret999",
            },
            format="json",
        )
        self.assertEqual(login_new.status_code, status.HTTP_200_OK)

    # 8) Password update requires auth token
    @patch("authentication.views.signup_view.send_verification_email")
    def test_password_update_requires_auth_and_updates(self, mock_send_email):
        user = self._signup_and_verify(mock_send_email)
        token, _ = Token.objects.get_or_create(user=user)

        unauth = self.client.post(
            self.update_url,
            {
                "current_password": self.user_payload["password"],
                "new_password": "updatedpass88",
            },
            format="json",
        )
        self.assertEqual(unauth.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
        response = self.client.post(
            self.update_url,
            {
                "current_password": self.user_payload["password"],
                "new_password": "updatedpass88",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.client.credentials()
        login = self.client.post(
            self.login_url,
            {
                "email": self.user_payload["email"],
                "password": "updatedpass88",
            },
            format="json",
        )
        self.assertEqual(login.status_code, status.HTTP_200_OK)
