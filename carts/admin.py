from django.contrib import admin

from .models import Cart, CartItem


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'user', 'status', 'created_at', 'updated_at']
    list_filter = ['status']
    search_fields = ['user__id']


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'cart', 'book', 'quantity', 'price']
    autocomplete_fields = ['cart', 'book']
    search_fields = ['cart__id', 'book__title']
