from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import UserProfile
from .forms import RegistrationForm, EditProfileForm, LoginForm


class UserTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.profile = UserProfile.objects.create(
            user=self.user, display_name="Test User"
        )
        self.client = Client()

    def test_registration_form(self):
        form = RegistrationForm(
            data={
                "username": "newuser",
                "password1": "newpassword1",
                "password2": "newpassword1",
                "email": "newuser@test.com",
                "display_name": "New User",
            }
        )
        self.assertTrue(form.is_valid())

    def test_edit_profile_form(self):
        form = EditProfileForm(
            data={"display_name": "Updated User", "email": "updated@test.com"},
            instance=self.profile,
        )
        self.assertTrue(form.is_valid())

    def test_login_form(self):
        form = LoginForm(data={"username": "testuser", "password": "testpassword"})
        self.assertTrue(form.is_valid())

    def test_login_view(self):
        response = self.client.post(
            reverse("users:login"),
            data={"username": "testuser", "password": "testpassword"},
        )
        self.assertEqual(response.status_code, 302)  # Expecting to redirect

    def test_register_view(self):
        response = self.client.post(
            reverse("users:register"),
            data={
                "username": "newuser",
                "password1": "newpassword1",
                "password2": "newpassword1",
                "email": "newuser@test.com",
                "display_name": "New User",
            },
        )
        self.assertEqual(response.status_code, 302)  # Expecting to redirect

    def test_profile_view(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse("users:profile"))
        self.assertEqual(response.status_code, 200)

    def test_profile_update_view(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(
            reverse("users:profile_update"),
            data={"display_name": "Updated User", "email": "updated@test.com"},
        )
        self.assertEqual(response.status_code, 302)  # Expecting to redirect

    def test_logout_view(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse("users:logout"))
        self.assertEqual(response.status_code, 302)  # Expecting to redirect

    def test_registration_form_invalid_data(self):
        form = RegistrationForm(
            data={
                "username": "",
                "password1": "password",
                "password2": "mismatch",
                "email": "invalid",
                "display_name": "User",
            }
        )
        self.assertFalse(form.is_valid())

    def test_edit_profile_form_invalid_data(self):
        form = EditProfileForm(
            data={"display_name": "", "email": "invalid"}, instance=self.profile
        )
        self.assertFalse(form.is_valid())

    def test_login_form_invalid_data(self):
        form = LoginForm(data={"username": "", "password": "wrongpassword"})
        self.assertFalse(form.is_valid())

    def test_login_view_failed_login(self):
        response = self.client.post(
            reverse("users:login"),
            data={"username": "testuser", "password": "wrongpassword"},
        )
        self.assertEqual(response.status_code, 200)  # Expecting to stay on the page

