from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        email = "test@fieldbox.ai"
        password = "test123"
        user = get_user_model().objects.create_user(
            email=email,
            password=password)
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalizer(self):
        """Test the email for a new user is normalizer"""
        email = "test@HIPPOLEV.AI"
        user = get_user_model().objects.create_user(email, "test123")
        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test if the user has an email address"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, "test123")

    def test_create_superuser_successful(self):
        """Test if creating a new superuser is successful"""
        user = get_user_model().objects.create_superuser(
            "hippolyte.leveque@gmail.com",
            "test123"
        )
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
