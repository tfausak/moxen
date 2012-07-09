from BeautifulSoup import BeautifulSoup
from collections import defaultdict
from django.template.defaultfilters import slugify
from magic.models import (Card, CardType, Color, ManaCost, ManaSymbol,
    Printing, Rarity, Ruling, Set, SubType, SuperType)
from magic.templatetags.magic_extras import title
from time import sleep
from urllib import urlencode, urlretrieve
from urllib2 import urlopen
import datetime
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


def tag_text(tag):
    """Extract all the text from a tag.

    If multiple text elements are found, they will be joined by a
    newline. Each text element will be stripped.
    """
    return '\n'.join(text.strip() for text in tag.findAll(text=True)).strip()


def scrape(set_):
    url = 'http://gatherer.wizards.com/Pages/Search/Default.aspx'
    parameters = {
        'set': '["{0}"]'.format(title(set_.name)),
        'special': 'true',
    }

    # Checklist
    checklist = []
    parameters['output'] = 'checklist'
    full_url = '{0}?{1}'.format(url, urlencode(parameters))
    print full_url
    response = urlopen(full_url)
    dom = BeautifulSoup(response)
    rows = dom.findAll('tr', 'cardItem') or []
    for row in rows:
        card = {}
        for key in ('number', 'name', 'artist', 'color', 'rarity', 'set'):
            card[key] = tag_text(row.find('td', key))
        card['multiverse_id'] = row.find('a', 'nameLink')['href'].split('=')[1]
        checklist.append(card)

    # Spoiler
    spoiler = {}
    parameters['output'] = 'spoiler'
    parameters['method'] = 'text'
    full_url = '{0}?{1}'.format(url, urlencode(parameters))
    print full_url
    response = urlopen(full_url)
    dom = BeautifulSoup(response)
    tag = dom.find('div', 'textspoiler')
    rows = tag.findAll('tr') or []
    card = {}
    multiverse_id = None
    for row in rows:
        cells = row.findAll('td')
        if len(cells) != 1:
            key = tag_text(cells[0])
            value = tag_text(cells[1])
            card[key] = value

            tag = row.find('a', 'nameLink')
            if tag:
                multiverse_id = tag['href'].split('=')[1]
        else:
            spoiler[multiverse_id] = card
            card = {}
            multiverse_id = None

    # Details
    details = {}
    url = 'http://gatherer.wizards.com/Pages/Card/Details.aspx'
    parameters = {}
    for multiverse_id in spoiler:
        card = {}
        parameters['multiverseid'] = multiverse_id
        full_url = '{0}?{1}'.format(url, urlencode(parameters))
        print full_url
        response = urlopen(full_url)
        sleep(1)
        dom = BeautifulSoup(response)

        rows = dom.findAll('div', 'row') or []
        for row in rows:
            key = tag_text(row.find('div', 'label'))
            value = tag_text(row.find('div', 'value'))
            card[key] = value

        tag = dom.find('div', id='ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_rulingsContainer')
        card['rulings'] = []
        if tag:
            rows = tag.findAll('tr') or []
            for row in rows:
                cells = row.findAll('td')
                card['rulings'].append({
                    'date': tag_text(cells[0]),
                    'text': tag_text(cells[1]),
                })

        details[multiverse_id] = card

    # Combine
    for card in checklist:
        multiverse_id = card['multiverse_id']
        for key, value in spoiler[multiverse_id].items():
            card[key] = value
        for key, value in details[multiverse_id].items():
            if key in ('rulings', 'Flavor Text:'):
                card[key] = value

    # Save
    cards = {}
    printings = {}
    for data in checklist:
        # fix keys
        data['cost'] = data['Cost:']
        data['hand_life'] = data.get('Hand/Life:', '')
        data['loyalty'] = data.get('Loyalty:', '')
        data['pow_tgh'] = data.get('Pow/Tgh:', '')
        data['rules_text'] = data['Rules Text:']
        data['set_rarity'] = data['Set/Rarity:']
        data['type'] = data['Type:']

        # find existing card or create shell
        # populate card values
        # save card
        data = _normalize_card(data)
        card = _store_card(data)
        cards[data['multiverse_id']] = card

        # find existing printing or create shell
        printing, _ = Printing.objects.get_or_create(card=card, set=set_,
            rarity=Rarity.objects.get(slug=data['rarity'].lower()),
            number=data['number'])
        # populate printing values
        printing.artist = data['artist'].lower()
        printing.flavor_text = data['Flavor Text:']
        # save printing
        printing.save()
        printings[data['multiverse_id']] = printing

        # look for rulings
        for ruling in data['rulings']:
            tokens = [int(token) for token in ruling['date'].split('/')]
            ruling['date'] = datetime.date(tokens[2], tokens[0], tokens[1])
            ruling, _ = Ruling.objects.get_or_create(**ruling)
            card.rulings.add(ruling)
        if data['rulings']:
            card.save()

        print printing

    # Images
    path = 'static/img/cards/{0}'.format(set_.slug)
    if not os.path.isdir(path):
        os.mkdir(path)
    url = 'http://gatherer.wizards.com/Handlers/Image.ashx'
    parameters = {'type': 'card'}
    for multiverse_id, printing in printings.items():
        path = 'static/img/cards/{0}/{1}-{2}.jpg'.format(
            printing.set.slug, printing.number, printing.card.slug)
        if not os.path.isfile(path):
            parameters['multiverseid'] = multiverse_id
            full_url = '{0}?{1}'.format(url, urlencode(parameters))
            print full_url
            urlretrieve(full_url, path)
            sleep(1)


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
