from django.urls import path

from .views import CurrentCart, add_to_cart

urlpatterns = [
    path('', CurrentCart.as_view(), name='current_cart'),
    path('add/<slug:slug>/', add_to_cart, name='add_to_cart'),
]
