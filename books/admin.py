from django.contrib import admin

from .models import Category, Publisher, Author


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ['name']}
    ordering = ['name']


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ['name']
    ordering = ['name']
    list_per_page = 25


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['full_name_reversed', 'full_name', 'slug']
    exclude = ['slug']
    ordering = ['last_name', 'first_name', 'middle_name']
    search_fields = ['last_name', 'first_name', 'middle_name']
