from django.shortcuts import render
from django.views.generic import DetailView, ListView
from magic.models import Card, Collection, Deck, Printing, Set


def index(request):
    """Display the home page.
    """
    return render(request, 'magic/index.html')


class CardListView(ListView):
    """Display a list of all the cards.
    """
    model = Card
    paginate_by = 60


class CardDetailView(DetailView):
    """Display a single card's details.
    """
    model = Card


class SearchView(CardListView):
    """Search for cards by name.
    """
    def get_queryset(self):
        self.query = self.request.GET.get('query')
        return Card.objects.filter(name__icontains=self.query)


class SetListView(ListView):
    """Display a list of all the sets.
    """
    model = Set

    def get_queryset(self):
        queryset = super(SetListView, self).get_queryset()
        queryset = queryset.order_by('-release_date')
        return queryset


class SetDetailView(DetailView):
    """Display a single set's details.
    """
    model = Set


class PrintingDetailView(DetailView):
    """Display a single printing's details.
    """
    model = Printing

    def get_object(self, **_):
        return Printing.objects.get(set__slug=self.kwargs['set_slug'],
            number=self.kwargs['number'], card__slug=self.kwargs['card_slug'])

    def get_context_data(self, **kwargs):
        context = super(PrintingDetailView, self).get_context_data(**kwargs)

        printings = Printing.objects.filter(set__slug=self.kwargs['set_slug'],
            number=int(self.kwargs['number']) - 1)
        try:
            context['previous_printing'] = printings.get()
        except Printing.DoesNotExist:
            context['previous_printing'] = None
        except Printing.MultipleObjectsReturned:
            context['previous_printing'] = printings[0]

        printings = Printing.objects.filter(set__slug=self.kwargs['set_slug'],
            number=int(self.kwargs['number']) + 1)
        try:
            context['next_printing'] = printings.get()
        except Printing.DoesNotExist:
            context['next_printing'] = None
        except Printing.MultipleObjectsReturned:
            context['next_printing'] = printings[0]

        return context


class DeckListView(ListView):
    """Display a list of all user-made decks.
    """
    model = Deck


class DeckDetailView(DetailView):
    """Display a single deck's details.
    """
    model = Deck


class CollectionDetailView(DetailView):
    """Display a single collection's details.
    """
    model = Collection
