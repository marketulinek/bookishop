from django.views.generic import TemplateView
from books.models import Book


class HomePageView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['new_books'] = Book.objects.select_related('author', 'bookinventory').order_by('-published_at')[:10]
        return context
