from django.test import TestCase

from books.models import Author, Book, Category, Publisher
from store.models import BookInventory, BookPrice


class CartTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create a book
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

        # Create a second book
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

    def test_add_to_basket_button_visibility_on_book_detail(self):
        # Book is NOT in stock and has NO price -> Button should NOT be visible
        with self.subTest('Book is not in stock'):
            response = self.client.get(self.harry_potter.get_absolute_url())
            self.assertEqual(response.status_code, 200)
            self.assertNotContains(response, '>Add to basket</a>')

        # Book is NOT in stock but has a price -> Button should NOT be visible
        with self.subTest('Book is not in stock'):
            BookPrice.objects.create(book=self.harry_potter, value=10.00, valid_from='2025-01-01')
            response = self.client.get(self.harry_potter.get_absolute_url())
            self.assertEqual(response.status_code, 200)
            self.assertNotContains(response, '>Add to basket</a>')

        # The book is in stock but has NO price -> Button should NOT be visible
        with self.subTest('Book in stock but no price'):
            BookInventory.objects.filter(book=self.cinder).update(quantity_in_hand=1)
            response = self.client.get(self.cinder.get_absolute_url())
            self.assertEqual(response.status_code, 200)
            self.assertNotContains(response, '>Add to basket</a>')

        # Book is in stock and has NO current price -> Button should NOT be visible
        with self.subTest('Book in stock with valid price'):
            BookPrice.objects.create(book=self.cinder, value=10.00, valid_from='2024-01-01', valid_until='2024-12-31')
            response = self.client.get(self.cinder.get_absolute_url())
            self.assertEqual(response.status_code, 200)
            self.assertNotContains(response, '>Add to basket</a>')

        # Book is in stock and has a valid price -> Button SHOULD be visible
        with self.subTest('Book in stock with valid price'):
            BookPrice.objects.create(book=self.cinder, value=10.00, valid_from='2025-01-01')
            response = self.client.get(self.cinder.get_absolute_url())
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, '>Add to basket</a>')
