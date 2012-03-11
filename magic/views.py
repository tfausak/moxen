from django.shortcuts import render
from django.template.defaultfilters import title
from django.views.generic import DetailView, ListView
from magic.models import Card


def index(request):
    """TODO
    """
    return render(request, 'magic/index.html')


class CardListView(ListView):
    """TODO
    """
    model = Card
    paginate_by = 100

    def get_context_data(self, **kwargs):
        context = super(CardListView, self).get_context_data(**kwargs)
        context['title'] = 'Cards'
        return context


class CardDetailView(DetailView):
    """TODO
    """
    model = Card

    def get_context_data(self, **kwargs):
        context = super(CardDetailView, self).get_context_data(**kwargs)
        context['title'] = title(self.object)
        return context
