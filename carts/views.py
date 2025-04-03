from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext as _
from django.views.decorators.http import require_POST
from django.views.generic import DetailView

from .models import Cart, CartStatus, CartItem
from books.models import Book
from core.http import HttpToastResponse
from core.utils import debug_print


class CurrentCart(LoginRequiredMixin, DetailView):
    template_name = 'cart.html'

    def get_object(self, queryset=None):
        return Cart.objects.filter(user=self.request.user, status=CartStatus.ACTIVE).first()


@require_POST
def add_to_cart(request, slug):

    if not request.user.is_authenticated:
        status, msg = 401, _('You have to be logged in.')
    else:
        try:
            book = Book.objects.get(slug=slug)
            CartItem.add_item(request.user, book)
            status, msg = 200, _('The book has been added to your cart.')
        except Book.DoesNotExist:
            status, msg = 400, _('The book does not exist.')
        except Exception as e:
            debug_print(f"Error: {e}")
            status, msg = 400, _('An error occurred.')

    return HttpToastResponse(status, msg).get_response()
