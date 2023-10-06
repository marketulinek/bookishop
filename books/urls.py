from django.urls import path

from .views import BookDetailView, CategoryListView, CategoryBookListView

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('categories/<slug:slug>/', CategoryBookListView.as_view(), name='books_by_category'),

    path('books/<slug:slug>/', BookDetailView.as_view(), name='book_detail')
]
