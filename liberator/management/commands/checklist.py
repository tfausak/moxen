from BeautifulSoup import BeautifulSoup
from django.core.management.base import BaseCommand
from magic.models import Card, Printing, Rarity, Set
from liberator.normalize import _normalize_string
from urllib2 import urlopen


class Command(BaseCommand):
    def handle(self, *args, **options):
        for url in args:
            checklist(url)


def checklist(url):
    try:
        response = open(url)
    except IOError:
        response = urlopen(url)
    dom = BeautifulSoup(response)
    rows = dom.findAll('tr', 'cardItem')
    for row in rows:
        card = dict((element['class'], element.findAll(text=True))
            for element in row.findAll('td'))
        for key, value in card.items():
            card[key] = _normalize_string('\n'.join(value))
        set_ = Set.objects.get(name=card['set'])
        rarity = Rarity.objects.get(slug=card['rarity'])
        number = int(card['number'] or 0)
        artist = card['artist']
        card = Card.objects.get(name=card['name'])

        try:
            printing = Printing.objects.get(card=card, set=set_, rarity=rarity,
                number=number)
        except Printing.DoesNotExist:
            try:
                printing = Printing.objects.get(card=card, set=set_,
                    rarity=rarity, number=0)
            except Printing.DoesNotExist:
                printing = Printing()

        printing.card = card
        printing.set = set_
        printing.rarity = rarity
        printing.number = number
        printing.artist = artist
        printing.save()
        print printing.number, printing, printing.artist
