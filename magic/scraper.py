from BeautifulSoup import BeautifulSoup
from collections import defaultdict
from django.template.defaultfilters import slugify
from magic.models import (Card, CardType, Color, ManaCost, ManaSymbol,
    Printing, Rarity, Set, SubType, SuperType)
from magic.templatetags.magic_extras import title
from urllib import urlencode, urlretrieve
from urllib2 import urlopen
import os
import re


# Every mana cost is made up of zero or more mana symbols.
MANA_SYMBOL = r'\d+|[wubrgxyzpstq]'
MANA_COST = re.compile(r'({0})|\(({0})/({0})\)'.format(MANA_SYMBOL))

# Every super type in the database with a pre-computed regex for
# matching against the type line.
SUPER_TYPES = []
for super_type in SuperType.objects.all():
    super_type.pattern = re.compile(
        r'\b{0}\b'.format(re.escape(super_type.name)))
    SUPER_TYPES.append(super_type)

# Every card type in the database with a pre-computed regex for matching
# against the type line.
CARD_TYPES = []
for card_type in CardType.objects.all():
    card_type.pattern = re.compile(
        r'\b{0}\b'.format(re.escape(card_type.name)))
    CARD_TYPES.append(card_type)

# Every sub type in the database with a pre-computed regex for matching
# against the type line.
SUB_TYPES = []
for sub_type in SubType.objects.all():
    sub_type.pattern = re.compile(
        r'\b{0}\b'.format(re.escape(sub_type.name)))
    SUB_TYPES.append(sub_type)

# Every set in the database with a pre-computed regex for matching
# against a set-rarity pair.
SETS = []
for set_ in Set.objects.all():
    set_.pattern = re.compile('^{0} '.format(re.escape(set_.name)))
    SETS.append(set_)
SETS.sort(key=lambda set_: len(set_.name), reverse=True)

# Every rarity in the database with a pre-computed regex for matching
# against a set-rarity pair.
RARITIES = []
for rarity in Rarity.objects.all():
    rarity.pattern = re.compile(' {0}$'.format(re.escape(rarity.name)))
    RARITIES.append(rarity)
RARITIES.sort(key=lambda rarity: len(rarity.name), reverse=True)


def scrape(set_):
    """Scrape a set's data from the Gatherer.
    """
    # Build a URL to the checklist for this set.
    url = 'http://gatherer.wizards.com/Pages/Search/'
    parameters = {
        'output': 'checklist',
        'set': '["{0}"]'.format(title(set_.name)),
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

            card['artists'] = [card['artist']]
            del card['artist']

            cards[card['name']] = card
        else:
            cards[card['name']]['numbers'].append(card['number'])
            cards[card['name']]['artists'].append(card['artist'])

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
        for number, artist in zip(card['numbers'], card['artists']):
            printing, _ = Printing.objects.get_or_create(
                card=card_,
                set=Set.objects.get(name=card['set']),
                rarity=Rarity.objects.get(slug=card['rarity']),
                number=number,
            )
            printing.artist = artist
            printing.save()
            cards[name]['printings'].append(printing)

    # Download card images.
    url_ = 'http://gatherer.wizards.com/Handlers/Image.ashx'
    parameters = {'type': 'card'}
    for name, card in cards.items():
        for printing in card['printings']:
            file_ = 'static/img/cards/{0}/{1}-{2}.jpg'.format(
                printing.set.slug, printing.number, printing.card.slug)
            if not os.path.isfile(file_):
                parameters['multiverseid'] = card['multiverse_id']
                url = '{0}?{1}'.format(url_, urlencode(parameters))
                urlretrieve(url, file_)


def _normalize_string(value, lower=True):
    """Normalize a string.
    """
    if not isinstance(value, basestring):
        return value

    value = value.strip()
    value = re.sub(r'\s+', ' ', value)
    if lower:
        value = value.lower()
    return value


def _normalize_int(value, default=0):
    """Normalize an integer.
    """
    try:
        return int(value)
    except ValueError:
        return default


def _normalize_card(card):
    """Normalize a single card's fields.
    """
    card = defaultdict(lambda: '', card)
    for key in ('name', 'cost', 'color', 'type', 'set_rarity', 'pow_tgh',
            'loyalty', 'hand_life'):
        card[key] = _normalize_string(card[key])

    # Name and slug
    match = re.search(r'\((.*)\)', card['name'])
    if match:
        card['name'] = match.group(1)
    card['slug'] = slugify(card['name'])

    # Mana cost
    card['cost'] = re.findall(MANA_COST, card['cost'])
    card['cost'] = [match[0] or '/'.join(match[1:]) for match in card['cost']]
    card['cost'] = [ManaSymbol.objects.get(name=mana_symbol)
        for mana_symbol in card['cost']]
    mana_symbols = defaultdict(lambda: 0)
    for mana_symbol in card['cost']:
        mana_symbols[mana_symbol] += 1
    card['mana_cost'] = []
    for mana_symbol, count in mana_symbols.items():
        mana_cost, _ = ManaCost.objects.get_or_create(
            mana_symbol=mana_symbol, count=count)
        card['mana_cost'].append(mana_cost)

    # Color(s)
    try:
        card['colors'] = [Color.objects.get(name=card['color'])]
    except Color.DoesNotExist:
        card['colors'] = set(color for mana_symbol in card['cost']
            for color in mana_symbol.colors.all())

    # Super, card, and sub types
    card['super_types'] = [type_ for type_ in SUPER_TYPES
        if re.search(type_.pattern, card['type'])]
    card['card_types'] = [type_ for type_ in CARD_TYPES
        if re.search(type_.pattern, card['type'])]
    card['sub_types'] = [type_ for type_ in SUB_TYPES
        if re.search(type_.pattern, card['type'])]

    # Sets and rarities
    card['set_rarity'] = card['set_rarity'].split(', ')
    sets, rarities = [], []
    for set_rarity in card['set_rarity']:
        for set_ in SETS:
            if re.search(set_.pattern, set_rarity):
                sets.append(set_)
                break
        for rarity in RARITIES:
            if re.search(rarity.pattern, set_rarity):
                rarities.append(rarity)
                break
    card['sets_rarities'] = zip(sets, rarities)

    # Rules text
    card['rules_text'] = [_normalize_string(line, lower=False)
        for line in card['rules_text'].split('\n')]
    card['rules_text'] = '\n'.join(line for line in card['rules_text'] if line)

    # Power and toughness
    try:
        card['power'], card['toughness'] = card['pow_tgh'][1:-1].split('/')
    except ValueError:
        card['power'] = card['toughness'] = ''

    # Loyalty
    card['loyalty'] = card['loyalty'][1:-1]

    # Hand and life modifiers
    try:
        card['hand_modifier'], card['life_modifier'] = re.findall(
            r'([+-]?\d+)', card['hand_life'])
    except ValueError:
        card['hand_modifier'] = card['life_modifier'] = ''

    # Calculate converted integer values for some fields.
    card['converted_power'] = _normalize_int(card['power'])
    card['converted_toughness'] = _normalize_int(card['toughness'])
    card['loyalty'] = _normalize_int(card['loyalty'])
    card['hand_modifier'] = _normalize_int(card['hand_modifier'])
    card['life_modifier'] = _normalize_int(card['life_modifier'])

    return card


def _store_card(data):
    """Store a single card.
    """
    card, _ = Card.objects.get_or_create(name=data['name'], slug=data['slug'])
    for key in ('rules_text', 'mana_cost', 'super_types', 'card_types',
            'sub_types', 'power', 'toughness', 'loyalty', 'hand_modifier',
            'life_modifier', 'colors', 'converted_power',
            'converted_toughness'):
        setattr(card, key, data[key])
    card.save()
    return card
