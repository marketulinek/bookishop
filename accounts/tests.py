from django.contrib.auth import get_user_model
from django.test import TestCase


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
