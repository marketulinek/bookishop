from django.contrib import admin

from .models import Publisher


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ['name']
    ordering = ['name']
    list_per_page = 25
