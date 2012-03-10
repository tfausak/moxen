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
    card['super_types'] = [super_type for pattern, super_type
        in liberator.constants.SUPER_TYPES if re.search(pattern, card['type'])]
    card['card_types'] = [card_type for pattern, card_type
        in liberator.constants.CARD_TYPES if re.search(pattern, card['type'])]
    card['sub_types'] = [sub_type for pattern, sub_type
        in liberator.constants.SUB_TYPES if re.search(pattern, card['type'])]

    # Power, toughness, loyalty, and hand and life modifiers
    card['power'] = card['toughness'] = ''
    card['loyalty'] = card['hand_modifier'] = card['life_modifier'] = 0
    if 'creature' in card['type']:
        match = re.search(r'\((.*)/(.*)\)', card['misc'])
        card['power'] = match.group(1)
        card['toughness'] = match.group(2)
    if 'planeswalker' in card['type']:
        match = re.search(r'\((\d+)\)', card['misc'])
        card['loyalty'] = int(match.group(1))
    if 'vanguard' in card['type']:
        matches = re.findall(r'([-+]\d+)', card['misc'])
        card['hand_modifier'] = int(matches[0])
        card['life_modifier'] = int(matches[1])

    return card
