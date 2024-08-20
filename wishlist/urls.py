from django.urls import path

from .views import WishlistListView, add_to_wishlist, remove_from_wishlist

urlpatterns = [
    path('', WishlistListView.as_view(), name='wishlist'),
    path('add/<slug:slug>/', add_to_wishlist, name='add_to_wishlist'),
    path('remove/<slug:slug>/', remove_from_wishlist, name='remove_from_wishlist'),
]
