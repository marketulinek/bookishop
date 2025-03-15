from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from accounts.models import CustomUser
from books.models import Book


class CartStatus(models.TextChoices):
    ACTIVE = 'active', _('Active')
    PURCHASED = 'purchased', _('Purchased')
    ABANDONED = 'abandoned', _('Abandoned')


class Cart(models.Model):
    user = models.ForeignKey(CustomUser, related_name='carts', on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=16, choices=CartStatus.choices, default=CartStatus.ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user'],
                name='unique_active_cart_per_user',
                condition=models.Q(status=CartStatus.ACTIVE)
            ),
            models.CheckConstraint(
                check=Q(user__isnull=False) | Q(status=CartStatus.ABANDONED),
                name='require_user_unless_abandoned'
            )
        ]

    def __str__(self):
        return f"Cart {self.id} - {self.user or 'Anonymous'} ({self.status})"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    book = models.ForeignKey(Book, related_name='cart_items', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['cart', 'book'], name='unique_cart_book')
        ]

    def __str__(self):
        return f"{self.quantity}x {self.book} in Cart {self.id}"
