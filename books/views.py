from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView

from .models import Book, Category


class CategoryListView(ListView):
    model = Category
    context_object_name = 'category_list'
    template_name = 'categories/category_list.html'


class CategoryBookListView(ListView):
    template_name = 'categories/books_by_category.html'
    context_object_name = 'books'

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'])
        return Book.objects.filter(category=self.category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


class BookDetailView(DetailView):
    model = Book
    context_object_name = 'book'
    template_name = 'books/book_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['book_details'] = self.get_book_details()
        return context

    def get_book_details(self):
        return {
            'Format': self.object.get_format_display,
            'Publisher': self.object.publisher,
            'Language': '-',
            'Publication Date': self.object.published_at,
            'Dimensions': '-',
            'ISBN10': '-',
            'Categories': self.object.category,
            'ISBN13': '-'
        }
