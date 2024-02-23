from django.test import TestCase

from .models import BookInventory
from books.models import Author, Book, Category, Publisher


class BookInventoryTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.publisher = Publisher.objects.create(name='Bloomsbury')
        cls.category = Category.objects.create(name='Fantasy', slug='fantasy')
        cls.author = Author.objects.create(first_name='Joanne', middle_name='K.', last_name='Rowling')
        cls.book = Book.objects.create(
            title='Harry Potter',
            author=cls.author,
            publisher=cls.publisher,
            category=cls.category,
            format='paperback',
            description='Boy Who Lived',
            published_at='1997-06-26',
        )
        cls.inventory = BookInventory.objects.create(
            book=cls.book,
            quantity_in_hand=100,
            quantity_to_be_delivered=50,
            min_stock_limit=20,
            max_stock_limit=200,
        )

    def test_book_inventory_model(self):
        self.assertEqual(self.book.title, 'Harry Potter')
        self.assertEqual(self.inventory.quantity_in_hand, 100)
        self.assertEqual(self.inventory.quantity_to_be_delivered, 50)
        self.assertEqual(self.inventory.min_stock_limit, 20)
        self.assertEqual(self.inventory.max_stock_limit, 200)
        self.assertEqual(self.inventory.reorder_point, 0)
        # Properties to be tested
        self.assertEqual(self.inventory.quantity_available, 150)
        self.assertTrue(self.inventory.for_sale)
        self.assertTrue(self.inventory.in_stock)

