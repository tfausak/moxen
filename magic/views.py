"""Functions for viewing cards.
"""
from django.shortcuts import render
from django.template.defaultfilters import title
from django.views.generic import DetailView, ListView
from magic.models import Card


def index(request):
    """Display the home page.
    """
    return render(request, 'magic/index.html')


class CardListView(ListView):
    """Display a list of all the cards.
    """
    model = Card
    paginate_by = 60

    def get_context_data(self, **kwargs):
        context = super(CardListView, self).get_context_data(**kwargs)
        context['title'] = 'Cards'
        return context


class CardDetailView(DetailView):
    """Display a single card's details.
    """
    model = Card

    def get_context_data(self, **kwargs):
        context = super(CardDetailView, self).get_context_data(**kwargs)
        context['title'] = title(self.object)
        return context
