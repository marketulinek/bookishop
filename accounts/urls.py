from django.urls import path

from .views import SignupPageView, add_to_wishlist

urlpatterns = [
    path('signup/', SignupPageView.as_view(), name='signup'),

    path('wishlist/add/<slug:slug>/', add_to_wishlist, name='add_to_wishlist'),
]
