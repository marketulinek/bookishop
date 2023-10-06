from django.contrib import admin

from .models import Author, Book, Category, Publisher


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


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'format', 'published_at', 'slug']
    autocomplete_fields = ['author', 'publisher']
    exclude = ['slug']
    list_filter = ['category']
    date_hierarchy = 'published_at'
