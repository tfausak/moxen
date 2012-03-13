"""Functions for converting card information into consistent values.
"""
from django.template.defaultfilters import slugify
import liberator.constants
import re


def normalize(cards):
    """Normalize a bunch of cards' fields.
    """
    return [_normalize_card(card) for card in cards]


def _normalize_card(card):
    """Normalize a single card's fields.
    """
    # Basic cleanup of string fields.
    card['name'] = card['name'].lower().strip()
    card['mana_cost'] = card['mana_cost'].lower().strip()
    card['type'] = card['type'].lower().strip()
    card['misc'] = card['misc'].lower().strip()
    card['sets_rarities'] = card['sets_rarities'].lower().strip()

    # Set default values.
    card['power'] = card['toughness'] = ''
    card['loyalty'] = card['hand_modifier'] = card['life_modifier'] = 0
    card['converted_mana_cost'] = 0
    card['converted_power'] = card['converted_toughness'] = 0

    # Name and slug
    match = re.search(r'\((.*)\)$', card['name'])
    if match:
        card['name'] = match.group(1)
    card['slug'] = slugify(card['name'])

    # Rules text
    card['rules_text'] = '\n'.join(line.strip() for line in card['rules_text'])
    card['rules_text'] = re.sub(r'\n{2,}', r'\n', card['rules_text'].strip())

    # Mana cost
    card['mana_cost'] = re.findall(
        liberator.constants.MANA_SYMBOL, card['mana_cost'])
    card['mana_cost'] = ['/'.join(symbols[0] or symbols[1:])
        for symbols in card['mana_cost']]
    card['mana_cost'] = ('(' + ')('.join(card['mana_cost']) + ')'
        if card['mana_cost'] else '')

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

    # Power, toughness, loyalty, and hand and life modifiers
    if card['misc']:
        if liberator.constants.CREATURE_CARD_TYPE in card['card_types']:
            card['power'], card['toughness'] = re.search(
                r'\((.+)/(.+)\)', card['misc']).groups()
        elif liberator.constants.PLANESWALKER_CARD_TYPE in card['card_types']:
            card['loyalty'] = re.search(r'\((.+)\)', card['misc']).group(1)
        elif liberator.constants.VANGUARD_CARD_TYPE in card['card_types']:
            card['hand_modifier'], card['life_modifier'] = re.findall(
                r'([-+]?\d+)', card['misc'])

    # Sets and rarities
    sets = []
    rarities = []
    for set_rarity in card['sets_rarities'].split(', '):
        for set_ in liberator.constants.SETS:
            if re.search(set_.pattern, set_rarity):
                sets.append(set_)
                break
        for rarity in liberator.constants.RARITIES:
            if re.search(rarity.pattern, set_rarity):
                rarities.append(rarity)
                break
    card['sets_rarities'] = zip(sets, rarities)

    # Color
    card['colors'] = [color for color
        in liberator.constants.COLORS
        if re.search(color.pattern, card['mana_cost'])]

    # Calculate "converted" values.
    card['converted_mana_cost'] = sum(
        max(liberator.constants.MANA_COST[symbol] for symbol in symbols)
        for symbols in re.findall(
            liberator.constants.MANA_SYMBOL, card['mana_cost']))
    try:
        card['converted_power'] = int(card['power'])
    except ValueError:
        pass
    try:
        card['converted_toughness'] = int(card['toughness'])
    except ValueError:
        pass

    return card
