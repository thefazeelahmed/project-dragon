"""
Auth logical API tests — idea sample (not framework testing).

Focus:
- business rules (inactive until verify, hashed token storage)
- side effects mocked (email send)
"""

from unittest.mock import patch

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from authentication.models import EmailVerification
from authentication.tokens import hash_token
from user.models import User


class AuthLogicAPITests(APITestCase):
    def setUp(self):
        self.signup_url = reverse("auth-signup")
        self.verify_url = reverse("auth-email-verify")
        self.login_url = reverse("auth-login")
        self.user_payload = {
            "name": "Fazeel",
            "email": "fazeel@example.com",
            "password": "secret12345",
        }

    # ------------------------------------------------------------------
    # 1) Signup: user inactive + token HASHED in DB + email mocked
    # ------------------------------------------------------------------
    @patch("authentication.views.signup_view.send_verification_email")
    def test_signup_creates_inactive_user_and_hashed_token(self, mock_send_email):
        response = self.client.post(self.signup_url, self.user_payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data["success"])

        user = User.objects.get(email=self.user_payload["email"])
        self.assertFalse(user.is_active)  # cannot login until verify

        # token email se aata — mock se raw token milta hai (DEBUG pe depend nahi)
        mock_send_email.assert_called_once()
        _called_user, raw_token = mock_send_email.call_args[0]

        verification = EmailVerification.objects.get(user=user, purpose="signup")
        # raw token must NOT be stored; only hash
        self.assertNotEqual(verification.token_hash, raw_token)
        self.assertEqual(verification.token_hash, hash_token(raw_token))

    # ------------------------------------------------------------------
    # 2) Verify: valid token activates user + marks token used
    # ------------------------------------------------------------------
    @patch("authentication.views.signup_view.send_verification_email")
    def test_verify_email_activates_user(self, mock_send_email):
        self.client.post(self.signup_url, self.user_payload, format="json")
        raw_token = mock_send_email.call_args[0][1]

        response = self.client.post(
            self.verify_url,
            {"token": raw_token},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user = User.objects.get(email=self.user_payload["email"])
        self.assertTrue(user.is_active)

        verification = EmailVerification.objects.get(user=user, purpose="signup")
        self.assertTrue(verification.is_used)

        # same token again should fail (one-time use)
        again = self.client.post(
            self.verify_url,
            {"token": raw_token},
            format="json",
        )
        self.assertEqual(again.status_code, status.HTTP_400_BAD_REQUEST)

    # ------------------------------------------------------------------
    # 3) Login: blocked before verify, works after verify (+ token)
    # ------------------------------------------------------------------
    @patch("authentication.views.signup_view.send_verification_email")
    def test_login_requires_verified_email(self, mock_send_email):
        self.client.post(self.signup_url, self.user_payload, format="json")
        raw_token = mock_send_email.call_args[0][1]

        # before verify → fail
        before = self.client.post(
            self.login_url,
            {
                "email": self.user_payload["email"],
                "password": self.user_payload["password"],
            },
            format="json",
        )
        self.assertEqual(before.status_code, status.HTTP_401_UNAUTHORIZED)

        # verify
        self.client.post(self.verify_url, {"token": raw_token}, format="json")

        # after verify → success + API token
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
