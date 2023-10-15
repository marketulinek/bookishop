from django.contrib import admin
from django.db import models
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.utils.text import slugify


class MissingSlugUrlSettingsAttribute(Exception):
    pass


class SlugUrl(models.Model):
    slug = models.SlugField(max_length=300, unique=True)

    class Meta:
        abstract = True

    class Settings:
        url_view_name = None

    def get_absolute_url(self):
        view_name = self.Settings.url_view_name
        if view_name is None:
            raise MissingSlugUrlSettingsAttribute(
                "Attribute 'url_view_name' is missing in class Settings."
            )
        return reverse(view_name, kwargs={'slug': self.slug})

    def generate_slug(self, from_field, prefix_length=8, prefix_allowed_chars='0123456789'):
        unique_prefix = get_random_string(prefix_length, prefix_allowed_chars)
        self.slug = slugify(f"{unique_prefix} {from_field}")


class Category(SlugUrl):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = 'Categories'

    class Settings:
        url_view_name = 'books_by_category'

    def __str__(self):
        return self.name


class Publisher(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Author(SlugUrl):
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, default='', blank=True)
    last_name = models.CharField(max_length=50)

    @property
    def full_name(self):
        name = f'{self.first_name} {self.middle_name} {self.last_name}'
        return name.replace('  ', ' ')

    @property
    @admin.display(description='Name')
    def full_name_reversed(self):
        name = f'{self.last_name}, {self.first_name} {self.middle_name}'
        return name.strip()

    def __str__(self):
        return self.full_name

    def save(self, *args, **kwargs):
        """
        Since the slug is created from all fields,
        it is (re)generated with each change.
        """
        self.generate_slug(self.full_name)
        super().save(*args, **kwargs)


class Book(SlugUrl):
    BOOK_FORMAT = [
        ('hardcover', 'Hardcover'),
        ('paperback', 'Paperback')
    ]

    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, related_name='books', on_delete=models.CASCADE)
    publisher = models.ForeignKey(Publisher, related_name='books', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name='books', on_delete=models.CASCADE)
    format = models.CharField(max_length=16, choices=BOOK_FORMAT)
    description = models.TextField(blank=True)
    published_at = models.DateField()
    cover = models.ImageField(upload_to='covers/', blank=True)

    class Settings:
        url_view_name = 'book_detail'

    def __str__(self):
        return self.title

    def is_published(self):
        # TODO: is_published() in Book model
        pass

    def year_of_publication(self):
        return self.published_at.year

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.generate_slug(self.title)
        super().save(*args, **kwargs)
