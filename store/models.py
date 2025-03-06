from django.contrib import admin
from django.db import models
from django.db.models import Q
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from books.models import Book


class BookPrice(models.Model):
    book = models.ForeignKey(Book, related_name='prices', on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    valid_from = models.DateField()
    valid_until = models.DateField(null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['book', 'valid_from', 'valid_until'])
        ]

    def __str__(self):
        return f"{self.value} EUR - {self.book}"

    @classmethod
    def get_current_price(cls, book):
        today = timezone.now().date()
        return cls.objects.filter(
            Q(valid_until__gte=today) | Q(valid_until__isnull=True),
            valid_from__lte=today,
            book=book
        ).order_by('valid_from').first()

    @classmethod
    def get_current_price_value(cls, book):
        price_object = cls.get_current_price(book)
        return price_object.value if price_object else None


class BookInventory(models.Model):
    INVENTORY_STATUS = {
        'unavailable': _('Unavailable'),
        'pre_order': _('Pre-order'),
        'in_stock': _('In Stock'),
        'out_of_stock': _('Out of Stock'),
    }

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

    @property
    def inventory_status_code(self):
        if not self.for_sale:
            # Book is not published yet
            # Or there are no plans to sell this book anymore
            return 'unavailable'

        if not self.book.is_published and self.in_stock:
            return 'pre_order'

        if self.in_stock:
            return 'in_stock'

        return 'out_of_stock'

    @property
    def inventory_status(self):
        """
        Status defined mainly for customers
        to be shown on the book detail page.
        """
        return self.INVENTORY_STATUS.get(self.inventory_status_code)

    @admin.display(boolean=True)
    def in_stock_admin(self):
        return self.in_stock

    @admin.display(boolean=True)
    def pre_order(self):
        return not self.book.is_published


# ------------------------------
#            SIGNALS
# ------------------------------

@receiver(post_save, sender=Book)
def create_book_inventory(sender, instance, created, **kwargs):
    if created:
        BookInventory.objects.create(book=instance)
