"""This is a back-of-the-napkin liberator. It's not production ready.

The goal here is to get everything in one step. Starting with the checklist gives us all the printing information. Combining that with the text spoilers gives us all the card information. Finally grabbing all the images is pretty simple.

Eventually, this should be usable through the web. After creating a new set, this should be run to populate the set.

The previous iteration of the liberator was geared towards getting information about 20,000 cards quickly and with the fewest number of requests. From here on out, everything is incremental.
"""
from BeautifulSoup import BeautifulSoup
from django.core.management.base import BaseCommand
from liberator.normalize import _normalize_int, _normalize_string, normalize
from liberator.parse import _parse_gatherer_text
from magic.models import Card, Printing, Rarity, Set
import os
import urllib
import urllib2


class Command(BaseCommand):
    def handle(self, *args, **options):
        # Specify which sets to get.
        sets = [
            'Duel Decks: Venser vs. Koth',
        ]

        # Build a Gatherer URL.
        url = 'http://gatherer.wizards.com/Pages/Search/'
        parameters = {
            'output': 'checklist',
            'set': ''.join('|["{0}"]'.format(set_) for set_ in sets),
            'special': True,
        }
        full_url = '{0}?{1}'.format(url, urllib.urlencode(parameters))

        # Get the page and parse the DOM.
        response = urllib2.urlopen(full_url)
        dom = BeautifulSoup(response)

        # Get information from the checklist.
        cards = {}
        printings = {}
        rows = dom.findAll('tr', 'cardItem')
        for row in rows:
            # Pull out relevant data.
            id_ = _normalize_int(
                row.find('td', 'name').find('a')['href'].split('=')[1])
            name = _normalize_string(row.find('td', 'name').find('a').string)
            set_ = _normalize_string(row.find('td', 'set').string)
            rarity = _normalize_string(row.find('td', 'rarity').string)
            number = _normalize_int(row.find('td', 'number').string)
            artist = _normalize_string(row.find('td', 'artist').string)

            # Get or create (but don't save!) Card object.
            try:
                card = Card.objects.get(name=name)
            except Card.DoesNotExist:
                print u'Creating card: {0}'.format(name)
                card = Card(name=name)
            cards[id_] = card

            # Get or create (but don't save!) Printing object.
            set_ = Set.objects.get(name=set_)
            rarity = Rarity.objects.get(slug=rarity)
            try:
                printing = Printing.objects.get(
                    card=card, set=set_, rarity=rarity, number=number)
            except Printing.DoesNotExist:
                print u'Creating printing: {0} {1} {2} {3}'.format(set_, rarity, number, card.name)
                printing = Printing(
                    card=card, set=set_, rarity=rarity, number=number)
            printings[id_] = printing

            print u'{0:3} {1} {2:3d} {3}'.format(set_.slug, rarity.slug, number, name)

        # Get information from text spoilers.
        parameters['output'] = 'spoiler'
        parameters['method'] = 'text'
        full_url = '{0}?{1}'.format(url, urllib.urlencode(parameters))
        response = urllib2.urlopen(full_url)
        spoilers = _parse_gatherer_text(response)
        spoilers = normalize(spoilers)
        for id_ in cards:
            card = cards[id_]
            printing = printings[id_]
            found = False
            for spoiler in spoilers:
                if spoiler['name'] == card.name:
                    found = True
                    break
            if not found:
                print u'Failed to match {0}'.format(card.name)
                continue

            # Set card details.
            for key in ('rules_text', 'mana_cost', 'super_types', 'card_types',
                    'sub_types', 'power', 'toughness', 'loyalty',
                    'hand_modifier', 'life_modifier', 'colors',
                    'converted_mana_cost', 'converted_power',
                    'converted_toughness'):
                setattr(card, key, spoiler[key])

            # Save everything.
            card.save()
            printing.save()

        # Get card images.
        for id_ in printings:
            printing = printings[id_]
            url_ = 'http://gatherer.wizards.com/Handlers/Image.ashx?type=card&multiverseid={0}'.format(id_)
            file_ = 'static/img/cards/{0}/{1}-{2}.jpg'.format(printing.set.slug, printing.number, printing.card.slug)
            if not os.path.isfile(file_):
                urllib.urlretrieve(url_, file_)
                print file_
