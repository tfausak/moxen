from collections import defaultdict
from django.template.defaultfilters import slugify
import liberator.constants
import re


def normalize(cards):
    """Normalize a bunch of cards' fields.
    """
    return [_normalize_card(card) for card in cards]


def _normalize_string(value, lower=True):
    """Normalize a string.
    """
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
    card['cost'] = re.findall(liberator.constants.MANA_SYMBOL, card['cost'])
    card['cost'] = ['/'.join(match[0] or match[1:]) for match in card['cost']]

    # Super, card, and sub types
    card['super_types'] = [super_type for super_type
        in liberator.constants.SUPER_TYPES
        if re.search(super_type.pattern, card['type'])]
    card['card_types'] = [card_type for card_type
        in liberator.constants.CARD_TYPES
        if re.search(card_type.pattern, card['type'])]
    card['sub_types'] = [sub_type for sub_type
        in liberator.constants.SUB_TYPES
        if re.search(sub_type.pattern, card['type'])]

    # Sets and rarities
    card['set_rarity'] = card['set_rarity'].split(', ')
    sets, rarities = [], []
    for set_rarity in card['set_rarity']:
        for set_ in liberator.constants.SETS:
            if re.search(set_.pattern, set_rarity):
                sets.append(set_)
                break
        for rarity in liberator.constants.RARITIES:
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
        card['power'], card['toughness'] = '/'.split(card['pow_tgh'])
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

    # Remove obsolete fields.
    for key in ('color', 'type', 'set_rarity', 'pow_tgh', 'hand_life'):
        del card[key]

    return card
