from django.shortcuts import get_object_or_404
from django.views.generic import ListView

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
