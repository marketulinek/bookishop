from django.urls import path

from .views import CurrentCart

urlpatterns = [
    path('', CurrentCart.as_view(), name='current_cart'),
]
