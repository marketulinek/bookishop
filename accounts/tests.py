from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .forms import CustomUserCreationForm


class CustomUserTests(TestCase):

    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            username='Kamila', email='kamilka@knihomolka.cz', password='knihomol123'
        )
        self.assertEqual(user.username, 'Kamila')
        self.assertEqual(user.email, 'kamilka@knihomolka.cz')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(
            username='Terka', email='terka@testerka.cz', password='testuji123'
        )
        self.assertEqual(admin_user.username, 'Terka')
        self.assertEqual(admin_user.email, 'terka@testerka.cz')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)


class SignUpPageTests(TestCase):
    def setUp(self):
        url = reverse('signup')
        self.response = self.client.get(url)

    def test_signup_template(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'registration/signup.html')
        self.assertContains(self.response, 'Sign Up')
        self.assertNotContains(self.response, 'This should not be on the page.')

    def test_signup_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, CustomUserCreationForm)
        self.assertContains(self.response, 'csrfmiddlewaretoken')
