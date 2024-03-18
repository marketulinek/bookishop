import json

from django.db.utils import IntegrityError
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views import generic
from django.views.decorators.http import require_http_methods

from .forms import CustomUserCreationForm
from .models import Wishlist
from books.models import Book


class SignupPageView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


@require_http_methods(['POST'])
def add_to_wishlist(request, slug):

    if not request.user.is_authenticated:
        toast = ('danger', _('You have to be logged in.'))
    else:
        try:
            book = Book.objects.get(slug=slug)
            Wishlist(user=request.user, book=book).save()
            toast = ('success', _('The book has been added to your wishlist.'))
        except Book.DoesNotExist:
            toast = ('danger', _('The book does not exist!'))
        except IntegrityError:
            toast = ('warning', _('The book is already on your wishlist.'))
        except Exception:
            toast = ('danger', _('An error occurred!'))

    return HttpResponse(status=204, headers={'HX-Trigger': json.dumps({
        'showMessage': {'level': toast[0], 'message': toast[1]}
    })})
