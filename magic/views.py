from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic import DetailView, ListView
from magic.models import Card, Set


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
    # pylint: disable=R0901,W0201
    def get_queryset(self):
        self.query = self.request.GET.get('query')
        return Card.objects.filter(name__icontains=self.query)


class SetListView(ListView):
    """Display a list of all the sets.
    """
    model = Set


class SetDetailView(DetailView):
    """Display a single set's details.
    """
    model = Set


@login_required
def profile(request):
    """Display a user's profile.
    """
    return render(request, 'magic/profile.html')
