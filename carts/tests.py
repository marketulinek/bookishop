from django.test import TestCase
from django.urls import reverse

from accounts.models import CustomUser
from books.models import Author, Book, Category, Publisher
from store.models import BookInventory, BookPrice


class AddToBasketButtonVisibilityTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create a book (signal sets book inventory quantity to 0)
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

        # Create a second book with inventory quantity 1
        cls.feiwel_friends = Publisher.objects.create(name='Feiwel & Friends')
        cls.meyer = Author.objects.create(first_name='Marissa', last_name='Meyer')
        cls.cinder = Book.objects.create(
            title='Cinder',
            author=cls.meyer,
            publisher=cls.feiwel_friends,
            category=cls.fantasy,
            format='hardcover',
            description='Cinder, a gifted mechanic, is a cyborg',
            published_at='2012-01-03'
        )
        BookInventory.objects.filter(book=cls.cinder).update(quantity_in_hand=1)

    def test_book_not_in_stock_without_price_not_visible(self):
        """Book is NOT in stock and has NO price -> Button should NOT be visible"""
        response = self._get_book_detail_response(self.harry_potter)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self._get_part_of_button_html())

    def test_book_not_in_stock_with_price_not_visible(self):
        """Book is NOT in stock but has a price -> Button should NOT be visible"""
        BookPrice.objects.create(book=self.harry_potter, value=10.00, valid_from='2025-01-01')
        response = self._get_book_detail_response(self.harry_potter)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self._get_part_of_button_html())

    def test_book_in_stock_without_price_not_visible(self):
        """The book is in stock but has NO price -> Button should NOT be visible"""
        response = self._get_book_detail_response(self.cinder)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self._get_part_of_button_html())

    def test_book_in_stock_without_current_price_not_visible(self):
        """Book is in stock and has NO current price -> Button should NOT be visible"""
        BookPrice.objects.create(book=self.cinder, value=10.00, valid_from='2024-01-01', valid_until='2024-12-31')
        response = self._get_book_detail_response(self.cinder)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self._get_part_of_button_html())

    def test_book_in_stock_with_current_price_visible(self):
        """Book is in stock and has a current price -> Button SHOULD be visible"""
        BookPrice.objects.create(book=self.cinder, value=10.00, valid_from='2025-01-01')
        response = self._get_book_detail_response(self.cinder)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self._get_part_of_button_html())

    def _get_book_detail_response(self, book):
        return self.client.get(book.get_absolute_url())

    @staticmethod
    def _get_part_of_button_html():
        return '>Add to basket</button>'


class CurrentCartPageTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.testerka = CustomUser.objects.create_user('testerka', 'testerka@bookishop.com', 'I.love.b00ks')

    def setUp(self):
        self.client.force_login(self.testerka)
        self.response = self.client.get(reverse('current_cart'))

    def test_anonymous_cannot_see_current_cart_page(self):
        self.client.logout()
        response = self.client.get(reverse('current_cart'))
        destination_url = '/accounts/login/?next=/en/cart/'
        self.assertRedirects(response, destination_url, target_status_code=302)

    def test_authenticated_user_can_see_current_cart_page(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'cart.html')
        self.assertContains(self.response, 'Cart')

    def test_user_has_empty_current_cart(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertContains(self.response, 'Your cart is empty')
