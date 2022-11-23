from django.test import TestCase
from django.contrib.auth import get_user_model

from unittest import skip

from accounts.authentication import PasswordlessAuthenticationBackend
from accounts.models import Token
from accounts.tests.test_views import TEST_EMAIL

User = get_user_model()


class AuthenticationTest(TestCase):
    
    def test_returns_None_if_no_such_token(self):
        result = PasswordlessAuthenticationBackend().authenticate(
            request=None,
            uid='no-such-token',
        )
        self.assertIsNone(result)

    def test_returns_new_user_with_correct_email_if_token_exists(self):
        email = TEST_EMAIL
        token = Token.objects.create(email=email)
        user = PasswordlessAuthenticationBackend().authenticate(
            request=None, 
            uid=token.uid
        )
        new_user = User.objects.get(email=email)
        self.assertEqual(user, new_user)

    def test_returns_existing_user_with_correct_email_if_token_exists(self):
        email = TEST_EMAIL
        existing_user = User.objects.create(email=email)
        token = Token.objects.create(email=email)
        user = PasswordlessAuthenticationBackend().authenticate(
            request=None, 
            uid=token.uid
        )
        self.assertEqual(user, existing_user)


class GetUserTest(TestCase):

    def test_gets_user_by_email(self):
        User.objects.create(email='another@example.com')
        desired_user = User.objects.create(email=TEST_EMAIL)
        found_user = PasswordlessAuthenticationBackend().get_user(TEST_EMAIL)
        self.assertEqual(found_user, desired_user)

    def test_returns_None_if_no_user_with_that_email(self):
        self.assertIsNone(
            PasswordlessAuthenticationBackend().get_user(TEST_EMAIL)
        )