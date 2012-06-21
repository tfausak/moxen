from BeautifulSoup import BeautifulSoup
from liberator.normalize import _normalize_card, _normalize_int, _normalize_string
from liberator.store import _store_card
from magic.models import Set, Rarity, Printing
from urllib import urlencode, urlretrieve
from urllib2 import urlopen
import os
import re


def scrape(set_):
    """Scrape a set's data from the Gatherer.
    """
    # Searching by set is case-sensitive when outputting the checklist.
    pattern = '\<(and|for|of|s|set|the|vs)\>'
    replacement = lambda match: match.group(1).lower()
    name = re.sub(pattern, replacement, set_.name.title())

    # Build a URL to the checklist for this set.
    url = 'http://gatherer.wizards.com/Pages/Search/'
    parameters = {
        'output': 'checklist',
        'set': '["{0}"]'.format(name),
        'special': 'true',
    }
    full_url = '{0}?{1}'.format(url, urlencode(parameters))

    # Get the checklist and parse the DOM.
    response = urlopen(full_url)
    dom = BeautifulSoup(response)

    # Collect card data from the checklist.
    rows = dom.findAll('tr', 'cardItem') or []
    cards = {}
    for row in rows:
        card = {
            'multiverse_id': row.find('a', 'nameLink')['href'].split('=')[1],
            'name': row.find('a', 'nameLink').string,
            'artist': row.find('td', 'artist').string,
            'color': row.find('td', 'color').string,
            'rarity': row.find('td', 'rarity').string,
            'set': row.find('td', 'set').string,
            'number': row.find('td', 'number').string,
        }
        for key in card:
            card[key] = _normalize_string(card[key])
        card['number'] = _normalize_int(card['number'])
        card['multiverse_id'] = _normalize_int(card['multiverse_id'])

        if card['name'] not in cards:
            card['numbers'] = [card['number']]
            del card['number']
            cards[card['name']] = card
        else:
            cards[card['name']]['numbers'].append(card['number'])

    # Build a URL to the text spoiler for this set.
    url = 'http://gatherer.wizards.com/Pages/Search/'
    parameters['method'] = 'text'
    parameters['output'] = 'spoiler'
    full_url = '{0}?{1}'.format(url, urlencode(parameters))

    # Get the text spoiler and parse the DOM.
    response = urlopen(full_url)
    dom = BeautifulSoup(response)

    # Collect card data from the text spoiler.
    rows = dom.find('div', 'textspoiler').findAll('tr') or []
    card = {}
    for row in rows:
        cells = row.findAll('td')
        if len(cells) != 1:
            key = re.sub('[^a-z]', '_', cells[0].string.strip().lower()[:-1])
            value = '\n'.join(text for text in cells[1].findAll(text=True))
            card[key] = value
        else:
            card = _normalize_card(card)
            for key, value in card.items():
                cards[card['name']][key] = value
            card = {}

    # Save cards and printings.
    for name, card in cards.items():
        card_ = _store_card(card)
        cards[name]['card'] = card_
        cards[name]['printings'] = []
        for number in card['numbers']:
            printing, _ = Printing.objects.get_or_create(
                card=card_,
                set=Set.objects.get(name=card['set']),
                rarity=Rarity.objects.get(slug=card['rarity']),
                number=number,
            )
            printing.artist = card['artist']
            printing.save()
            cards[name]['printings'].append(printing)

    # Download card images.
    for name, card in cards.items():
        url_ = 'http://gatherer.wizards.com/Handlers/Image.ashx'
        parameters = {
            'type': 'card',
            'multiverseid': card['multiverse_id'],
        }
        url = '{0}?{1}'.format(url_, urlencode(parameters))

        for printing in card['printings']:
            file_ = 'static/img/cards/{0}/{1}-{2}.jpg'.format(
                printing.set.slug, printing.number, printing.card.slug)
            if not os.path.isfile(file_):
                print url, '->', file_
                urlretrieve(url, file_)
