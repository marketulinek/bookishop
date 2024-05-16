from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .forms import CustomUserCreationForm
from .models import CustomUser, Wishlist
from books.models import Author, Book, Category, Publisher


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


class WishlistForAnonymousUserTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.bloomsbury = Publisher.objects.create(name='Bloomsbury')
        cls.fantasy = Category.objects.create(name='Fantasy', slug='fantasy')
        cls.rowling = Author.objects.create(first_name='Joanne', middle_name='K.', last_name='Rowling')
        cls.harry_potter = Book.objects.create(
            title='Harry Potter',
            author=cls.rowling,
            publisher=cls.bloomsbury,
            category=cls.fantasy,
            format='paperback',
            description='Boy Who Lived',
            published_at='1997-06-26'
        )

    def test_anonymous_cannot_see_wishlist_page(self):
        response = self.client.get(reverse('wishlist'))
        destination_url = '/accounts/login/?next=/en/accounts/wishlist/'
        self.assertRedirects(response, destination_url, target_status_code=302)

    def test_add_to_wishlist_button_visibility(self):
        """Tests the button located on the book detail page.

        The button should be always visible when the user is anonymous
        to show him that the feature exists."""
        response = self.client.get(self.harry_potter.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '>Add to wishlist</button>')

    def test_add_to_wishlist_method_get_not_allowed(self):
        response = self.client.get(reverse('add_to_wishlist', args=[self.harry_potter.slug]))
        self.assertEqual(response.status_code, 405)

    def test_add_to_wishlist_auth_required(self):
        response = self.client.post(reverse('add_to_wishlist', args=[self.harry_potter.slug]))
        self.assertEqual(response.status_code, 401)

    def test_remove_from_wishlist_method_get_not_allowed(self):
        response = self.client.get(reverse('remove_from_wishlist', args=[self.harry_potter.slug]))
        self.assertEqual(response.status_code, 405)

    def test_remove_from_wishlist_auth_required(self):
        response = self.client.post(reverse('remove_from_wishlist', args=[self.harry_potter.slug]))
        self.assertEqual(response.status_code, 401)


class WishlistForAuthenticatedUserTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.testerka = CustomUser.objects.create_user('testerka', 'terka.testerka@bookishop.com', 'I.love.b00ks')
        cls.bloomsbury = Publisher.objects.create(name='Bloomsbury')
        cls.feiwel_friends = Publisher.objects.create(name='Feiwel & Friends')
        cls.fantasy = Category.objects.create(name='Fantasy', slug='fantasy')
        cls.rowling = Author.objects.create(first_name='Joanne', middle_name='K.', last_name='Rowling')
        cls.meyer = Author.objects.create(first_name='Marissa', last_name='Meyer')

        cls.harry_potter = Book.objects.create(
            title='Harry Potter',
            author=cls.rowling,
            publisher=cls.bloomsbury,
            category=cls.fantasy,
            format='paperback',
            description='Boy Who Lived',
            published_at='1997-06-26'
        )
        cls.cinder = Book.objects.create(
            title='Cinder',
            author=cls.meyer,
            publisher=cls.feiwel_friends,
            category=cls.fantasy,
            format='hardcover',
            description='Cinder, a gifted mechanic, is a cyborg',
            published_at='2012-01-03'
        )

    def setUp(self):
        self.client.force_login(self.testerka)

    def test_authenticated_user_can_see_wishlist_page(self):
        response = self.client.get(reverse('wishlist'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Wishlist')
        self.assertTemplateUsed(response, 'wishlist.html')

    def test_user_has_empty_wishlist(self):
        response = self.client.get(reverse('wishlist'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "You don't have any books on your wishlist")
        self.assertNotContains(response, self.harry_potter.title)

    def test_user_has_book_on_wishlist(self):
        Wishlist.objects.create(user=self.testerka, book=self.harry_potter)
        response = self.client.get(reverse('wishlist'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.harry_potter.title)
        self.assertNotContains(response, "You don't have any books on your wishlist")

    def test_add_to_wishlist_button_visibility(self):
        """Tests the button located on the book detail page"""
        button_part = '>Add to wishlist</button>'
        Wishlist.objects.create(user=self.testerka, book=self.harry_potter)

        # Cinder is not on the user's wishlist -> button should be visible
        r_cinder = self.client.get(self.cinder.get_absolute_url())
        self.assertEqual(r_cinder.status_code, 200)
        self.assertContains(r_cinder, button_part)

        # Harry Potter is on the user's wishlist -> button should not be visible
        r_harry_potter = self.client.get(self.harry_potter.get_absolute_url())
        self.assertEqual(r_harry_potter.status_code, 200)
        self.assertNotContains(r_harry_potter, button_part)

    def test_add_to_wishlist_method_get_not_allowed(self):
        response = self.client.get(reverse('add_to_wishlist', args=[self.harry_potter.slug]))
        self.assertEqual(response.status_code, 405)

    def test_add_to_wishlist_method_post(self):
        old_count = Wishlist.objects.count()
        response = self.client.post(reverse('add_to_wishlist', args=[self.cinder.slug]))
        self.assertEqual(response.status_code, 200)
        new_count = Wishlist.objects.count()
        self.assertEqual(new_count, old_count + 1)

    def test_add_to_wishlist_book_does_not_exist(self):
        response = self.client.post(reverse('add_to_wishlist', args=['non-existent-slug']))
        self.assertEqual(response.status_code, 400)

    def test_add_to_wishlist_book_already_added(self):
        response = self.client.post(reverse('add_to_wishlist', args=[self.harry_potter.slug]))
        self.assertEqual(response.status_code, 200)

    def test_remove_from_wishlist_method_get_not_allowed(self):
        response = self.client.get(reverse('remove_from_wishlist', args=[self.harry_potter.slug]))
        self.assertEqual(response.status_code, 405)

    def test_remove_from_wishlist_method_post(self):
        Wishlist.objects.create(user=self.testerka, book=self.harry_potter)
        old_count = Wishlist.objects.count()
        response = self.client.post(reverse('remove_from_wishlist', args=[self.harry_potter.slug]))
        self.assertEqual(response.status_code, 200)
        new_count = Wishlist.objects.count()
        self.assertEqual(new_count, old_count - 1)
