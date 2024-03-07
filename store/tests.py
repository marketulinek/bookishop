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

        # Book inventory should be created by signal during book creation
        cls.inventory = BookInventory.objects.all()[0]

    def test_book_inventory_model(self):
        self.assertEqual(self.book.title, 'Harry Potter')
        self.assertEqual(self.inventory.quantity_in_hand, 0)
        self.assertEqual(self.inventory.quantity_to_be_delivered, 0)
        self.assertEqual(self.inventory.min_stock_limit, 0)
        self.assertEqual(self.inventory.max_stock_limit, 0)
        self.assertEqual(self.inventory.reorder_point, 0)
        # Properties to be tested
        self.assertEqual(self.inventory.quantity_available, 0)
        self.assertFalse(self.inventory.for_sale)
        self.assertFalse(self.inventory.in_stock)
