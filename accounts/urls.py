from django.urls import path

from .views import SignupPageView, WishlistListView, add_to_wishlist, remove_from_wishlist

urlpatterns = [
    path('signup/', SignupPageView.as_view(), name='signup'),

    path('wishlist/', WishlistListView.as_view(), name='wishlist'),
    path('wishlist/add/<slug:slug>/', add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<slug:slug>/', remove_from_wishlist, name='remove_from_wishlist'),
]
