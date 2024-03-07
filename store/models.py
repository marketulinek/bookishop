from django.contrib import admin
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from books.models import Book


class BookInventory(models.Model):
    book = models.OneToOneField(Book, on_delete=models.CASCADE, primary_key=True)
    quantity_in_hand = models.PositiveIntegerField(default=0)

    # Number of books ordered from the supplier.
    # This value, together with quantity_in_hand, should not exceed max_stock_limit.
    quantity_to_be_delivered = models.PositiveIntegerField(default=0)

    # TODO: When book units go under this point, send warning email (by signal?)
    min_stock_limit = models.PositiveIntegerField(default=0)

    # When value is zero, it means that there are no plans
    # to sell this book anymore.
    max_stock_limit = models.PositiveIntegerField(default=0)

    # When book units (quantity_available) reach this point,
    # the purchase order to supplier must be generated (TODO).
    reorder_point = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = 'Book Inventory'

    def __str__(self):
        return self.book.title

    @property
    def quantity_available(self):
        return self.quantity_in_hand + self.quantity_to_be_delivered

    @property
    def for_sale(self):
        return self.max_stock_limit > 0 or self.quantity_available > 0

    @property
    def in_stock(self):
        return self.quantity_available > 0

    @admin.display(boolean=True)
    def in_stock_admin(self):
        return self.in_stock

    @admin.display(boolean=True)
    def pre_order(self):
        return not self.book.is_published

    @property
    def inventory_status(self):
        """
        Status defined mainly for customers
        to be shown on the book detail page.
        """
        if not self.for_sale:
            # Book is not published yet
            # Or there are no plans to sell this book anymore
            return _('Unavailable')

        if not self.book.is_published and self.in_stock:
            return _('Pre-order')

        if self.in_stock:
            return _('In Stock')

        return _('Out of Stock')


# ------------------------------
#            SIGNALS
# ------------------------------

@receiver(post_save, sender=Book)
def create_book_inventory(sender, instance, created, **kwargs):
    if created:
        BookInventory.objects.create(book=instance)
