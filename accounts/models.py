from django.contrib.auth.models import AbstractUser
from django.db import models

from books.models import Book


class CustomUser(AbstractUser):
    pass


class Wishlist(models.Model):
    user = models.ForeignKey(CustomUser, related_name='_users', on_delete=models.CASCADE)
    book = models.ForeignKey(Book, related_name='_books', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    # class Meta:
    #     constraints = [
    #         models.UniqueConstraint(fields=['user', 'book'], name='unique_user_book')
    #     ]

    def __str__(self):
        return f'{self.user} likes {self.book}'
