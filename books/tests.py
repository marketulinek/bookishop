from django.test import TestCase

from .models import Author


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
