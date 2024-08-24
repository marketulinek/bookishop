from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.utils import IntegrityError
from django.utils.translation import gettext as _
from django.views.generic import ListView
from django.views.decorators.http import require_http_methods

from .models import Wishlist
from books.models import Book
from core.http import HttpToastResponse


class WishlistListView(LoginRequiredMixin, ListView):
    context_object_name = 'wishlist'
    template_name = 'wishlist.html'

    def get_queryset(self):
        wishlist = Wishlist.objects.filter(user=self.request.user)
        return wishlist.select_related('book').select_related('book__author').select_related('book__bookinventory')


@require_http_methods(['POST'])
def add_to_wishlist(request, slug):

    if not request.user.is_authenticated:
        status, msg = 401, _('You have to be logged in.')
    else:
        try:
            book = Book.objects.get(slug=slug)
            Wishlist(user=request.user, book=book).save()
            status, msg = 200, _('The book has been added to your wishlist.')
        except IntegrityError:
            status, msg = 200, _('The book is already on your wishlist.')
        except Book.DoesNotExist:
            status, msg = 400, _('The book does not exist.')
        except Exception:
            status, msg = 400, _('An error occurred.')

    return HttpToastResponse(status, msg).get_response()


@require_http_methods(['POST'])
def remove_from_wishlist(request, slug):

    if not request.user.is_authenticated:
        status, msg = 401, _('You have to be logged in.')
    else:
        try:
            book = Book.objects.get(slug=slug)
            Wishlist.objects.get(user=request.user, book=book).delete()
            status, msg = 200, _('The book has been removed from your wishlist.')
        except Book.DoesNotExist:
            status, msg = 400, _('The book does not exist.')
        except Exception:
            status, msg = 400, _('An error occurred.')

    return HttpToastResponse(status, msg).get_response()
