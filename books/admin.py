from django.contrib import admin

from .models import Author, Book, Category, Publisher
from store.models import BookInventory


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ['name']}
    ordering = ['name']


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ['name']
    ordering = ['name']
    search_fields = ['name']
    list_per_page = 25


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['full_name_reversed', 'full_name', 'slug']
    exclude = ['slug']
    ordering = ['last_name', 'first_name', 'middle_name']
    search_fields = ['last_name', 'first_name', 'middle_name']


class BookInventoryInline(admin.StackedInline):
    model = BookInventory
    fields = [
        'inventory_status',
        ('quantity_in_hand', 'quantity_to_be_delivered', 'quantity_available'),
        ('min_stock_limit', 'max_stock_limit', 'reorder_point')
    ]
    readonly_fields = ['inventory_status', 'quantity_available']


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'format', 'published_at']
    autocomplete_fields = ['author', 'publisher']
    exclude = ['slug']
    list_filter = ['category']
    date_hierarchy = 'published_at'
    inlines = [BookInventoryInline]
