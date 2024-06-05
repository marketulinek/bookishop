import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.utils import IntegrityError
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic import ListView, CreateView
from django.views.decorators.http import require_http_methods

from .forms import CustomUserCreationForm
from .models import Wishlist
from books.models import Book


class SignupPageView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


class WishlistListView(LoginRequiredMixin, ListView):
    context_object_name = 'wishlist'
    template_name = 'wishlist.html'

    def get_queryset(self):
        wishlist = Wishlist.objects.filter(user=self.request.user)
        return wishlist.select_related('book').select_related('book__author').select_related('book__bookinventory')


@require_http_methods(['POST'])
def add_to_wishlist(request, slug):

    if not request.user.is_authenticated:
        toast = ('danger', _('You have to be logged in.'))
        status_code = 401
    else:
        try:
            book = Book.objects.get(slug=slug)
            Wishlist(user=request.user, book=book).save()
            toast = ('success', _('The book has been added to your wishlist.'))
            status_code = 200
        except IntegrityError:
            toast = ('warning', _('The book is already on your wishlist.'))
            status_code = 200
        except Book.DoesNotExist:
            toast = ('danger', _('The book does not exist.'))
            status_code = 400
        except Exception:
            toast = ('danger', _('An error occurred.'))
            status_code = 400

    return HttpResponse(status=status_code, headers={'HX-Trigger': json.dumps({
        'showMessage': {'level': toast[0], 'message': toast[1]}
    })})


@require_http_methods(['POST'])
def remove_from_wishlist(request, slug):

    if not request.user.is_authenticated:
        toast = ('danger', _('You have to be logged in.'))
        status_code = 401
    else:
        try:
            book = Book.objects.get(slug=slug)
            Wishlist.objects.get(user=request.user, book=book).delete()
            toast = ('success', _('The book has been removed from your wishlist.'))
            status_code = 200
        except Book.DoesNotExist:
            toast = ('danger', _('The book does not exist.'))
            status_code = 400
        except Exception:
            toast = ('danger', _('An error occurred.'))
            status_code = 400

    return HttpResponse(status=status_code, headers={'HX-Trigger': json.dumps({
        'showMessage': {'level': toast[0], 'message': toast[1]}
    })})
