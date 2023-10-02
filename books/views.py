from django.views.generic import ListView

from .models import Category


class CategoryListView(ListView):
    model = Category
    context_object_name = 'category_list'
    template_name = 'categories/category_list.html'
