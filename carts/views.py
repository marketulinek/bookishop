from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView

from .models import Cart, CartStatus


class CurrentCart(LoginRequiredMixin, DetailView):
    template_name = 'cart.html'

    def get_object(self, queryset=None):
        return Cart.objects.filter(user=self.request.user, status=CartStatus.ACTIVE).first()
