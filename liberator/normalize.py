from django.template.defaultfilters import slugify
from magic.models import CardType, SubType, SuperType
import liberator.constants
import re


def normalize(cards):
    """Normalize a bunch of cards' fields.
    """
    return [_normalize_card(card) for card in cards]


def _normalize_card(card):
    """Normalize a single card's fields.
    """
    # Name
    card['name'] = re.sub('\s+', ' ', card['name'].lower().strip())
    match = re.search(r'\((.*)\)$', card['name'])
    if match:
        card['name'] = match.group(1)

    # Slug
    card['slug'] = slugify(card['name'])

    # Rules text
    card['rules_text'] = '\n'.join(line.strip() for line in card['rules_text'])

    # Mana cost
    card['mana_cost'] = re.findall(
        r'({0})|\(({0})/({0})\)'.format(liberator.constants.MANA_SYMBOL),
        card['mana_cost'].lower().strip())
    card['mana_cost'] = '}{'.join('/'.join((x,) if x else (y, z))
        for x, y, z in card['mana_cost'])
    if card['mana_cost']:
        card['mana_cost'] = '{' + card['mana_cost'] + '}'

    # Type
    card['type'] = card['type'].lower().strip()
    card['super_types'] = [super_type for super_type in SuperType.objects.all()
        if super_type.name in card['type']]
    card['card_types'] = [card_type for card_type in CardType.objects.all()
        if card_type.name in card['type']]
    card['sub_types'] = [sub_type for sub_type in SubType.objects.all()
        if sub_type.name in card['type']]

    # Power, toughness, loyalty, and hand and life modifiers
    card['power'] = card['toughness'] = card['loyalty'] = \
        card['hand_modifier'] = card['life_modifier'] = ''
    if 'creature' in card['type']:
        match = re.findall(r'\((.*)/(.*)\)', card['misc'])
        card['power'] = match[0][0]
        card['toughness'] = match[0][1]
    if 'planeswalker' in card['type']:
        card['loyalty'] = card['misc']
    if 'vanguard' in card['type']:
        match = re.findall(r'\((.*)/(.*)\)', card['misc'])
        card['hand_modifier'] = match[0][0]
        card['life_modifier'] = match[0][1]

    return card
