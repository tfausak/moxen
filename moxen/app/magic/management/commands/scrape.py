from django.core.management.base import BaseCommand
from django.db.models import Q
from magic.models import Set
from magic.scraper import scrape


class Command(BaseCommand):
    """Convenience command to scrape sets from the command line.
    """
    args = 'set ...'
    help = 'Scrape the given sets.'

    def handle(self, *args, **options):
        for arg in args:
            arg = arg.lower()
            try:
                set_ = Set.objects.get(Q(code=arg) | Q(name=arg) | Q(slug=arg))
            except Set.DoesNotExist:
                continue

            print set_.name
            scrape(set_)
