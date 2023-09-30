from django.contrib import admin
from django.db import models
from django.utils.crypto import get_random_string
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Publisher(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Author(models.Model):
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, default='', blank=True)
    last_name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=200, unique=True)

    @property
    def full_name(self):
        name = f'{self.first_name} {self.middle_name} {self.last_name}'
        return ' '.join(name.split())

    @property
    @admin.display(description='Name')
    def full_name_reversed(self):
        name = f'{self.last_name}, {self.first_name} {self.middle_name}'
        return ' '.join(name.split())

    def __str__(self):
        return self.full_name

    def save(self, *args, **kwargs):
        """
        Since the slug is created from all fields,
        it is (re)generated with each change.
        """
        new_slug = f"{get_random_string(8, allowed_chars='0123456789')} {self.full_name}"
        self.slug = slugify(new_slug)
        super().save(*args, **kwargs)
