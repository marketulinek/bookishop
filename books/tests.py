from django.test import TestCase
from django.urls import reverse

from .models import Author, Book, Category, Publisher


class CategoryTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create(
            name='Fantasy',
            slug='fantasy'
        )

    def test_category_model(self):
        self.assertEqual(self.category.name, 'Fantasy')
        self.assertEqual(self.category.slug, 'fantasy')

    def test_category_list_view(self):
        response = self.client.get(reverse('category_list'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Fantasy')
        self.assertTemplateUsed(response, 'categories/category_list.html')

    def test_category_book_list_view(self):
        response = self.client.get(self.category.get_absolute_url())
        no_response = self.client.get('categories/lorem-ipsum')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Fantasy')
        self.assertContains(response, 'There are no books in this category :-(')
        self.assertNotContains(response, 'Harry Potter')
        self.assertTemplateUsed(response, 'categories/books_by_category.html')
        self.assertEqual(no_response.status_code, 404)


class AuthorTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = Author.objects.create(
            first_name='Joanne',
            middle_name='K.',
            last_name='Rowling'
        )

    def test_author_model(self):
        self.assertEqual(self.author.first_name, 'Joanne')
        self.assertEqual(self.author.middle_name, 'K.')
        self.assertEqual(self.author.last_name, 'Rowling')
        self.assertEqual(self.author.full_name, 'Joanne K. Rowling')
        self.assertEqual(self.author.full_name_reversed, 'Rowling, Joanne K.')
        self.assertEqual(self.author.slug[8:], '-joanne-k-rowling')


class BookTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.publisher = Publisher.objects.create(name='Bloomsbury')
        cls.category = Category.objects.create(name='Fantasy', slug='fantasy')

        cls.author = Author.objects.create(
            first_name='Joanne',
            middle_name='K.',
            last_name='Rowling'
        )

        cls.book = Book.objects.create(
            title='Harry Potter',
            author=cls.author,
            publisher=cls.publisher,
            category=cls.category,
            format='paperback',
            description='Boy Who Lived',
            published_at='1997-06-26'
        )

    def test_book_model(self):
        self.assertEqual(self.book.title, 'Harry Potter')
        self.assertEqual(self.book.author.full_name, 'Joanne K. Rowling')
        self.assertEqual(self.book.publisher.name, 'Bloomsbury')
        self.assertEqual(self.book.category.name, 'Fantasy')
        self.assertEqual(self.book.format, 'paperback')
        self.assertEqual(self.book.description, 'Boy Who Lived')
        self.assertEqual(self.book.published_at, '1997-06-26')

    def test_books_by_category_list_view(self):
        response = self.client.get(self.category.get_absolute_url())
        no_response = self.client.get('categories/lorem-ipsum')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Fantasy')
        self.assertContains(response, 'Harry Potter')
        self.assertNotContains(response, 'There are no books in this category :-(')
        self.assertTemplateUsed(response, 'categories/books_by_category.html')
        self.assertEqual(no_response.status_code, 404)

    def test_book_detail_view(self):
        response = self.client.get(self.book.get_absolute_url())
        no_response = self.client.get('books/lorem-ipsum')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Fantasy')
        self.assertContains(response, 'Harry Potter')
        self.assertNotContains(response, 'This should not be on the page.')
        self.assertTemplateUsed(response, 'books/book_detail.html')
        self.assertEqual(no_response.status_code, 404)
