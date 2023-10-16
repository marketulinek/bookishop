from django.test import TestCase
from django.urls import reverse

from books.models import Author, Book, Category, Publisher


class HomepageTests(TestCase):

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

    def test_homepage(self):
        response = self.client.get(reverse('home'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        self.assertContains(response, 'New books')
        self.assertNotContains(response, 'This should not be on the page.')
