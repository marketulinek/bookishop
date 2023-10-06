from django.test import TestCase
from django.urls import reverse

from .models import Author, Category


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
