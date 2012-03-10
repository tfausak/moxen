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
    card['converted_mana_cost'] = sum(max(
            liberator.constants.MANA_COST[symbol] for symbol in symbols)
        for symbols in card['mana_cost'])
    card['mana_cost'] = '}{'.join('/'.join((x,) if x else (y, z))
        for x, y, z in card['mana_cost'])
    if card['mana_cost']:
        card['mana_cost'] = '{' + card['mana_cost'] + '}'

    # Super, card, and sub types
    card['type'] = card['type'].lower().strip()
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
    card['power'] = card['toughness'] = ''
    card['loyalty'] = card['hand_modifier'] = card['life_modifier'] = 0
    if liberator.constants.CREATURE_CARD_TYPE in card['card_types']:
        card['power'], card['toughness'] = re.search(
            r'\((.+)/(.+)\)', card['misc']).groups()
    elif liberator.constants.PLANESWALKER_CARD_TYPE in card['card_types']:
        card['loyalty'] = re.search(r'\((.+)\)', card['misc']).group(1)
    elif liberator.constants.VANGUARD_CARD_TYPE in card['card_types']:
        card['hand_modifier'], card['life_modifier'] = re.findall(
            r'([-+]?\d+)', card['misc'])

    # Derived fields.
    card['colors'] = [color for color
        in liberator.constants.COLORS
        if re.search(color.pattern, card['mana_cost'])]
    try:
        card['converted_power'] = int(card['power'])
    except ValueError:
        card['converted_power'] = 0
    try:
        card['converted_toughness'] = int(card['toughness'])
    except ValueError:
        card['converted_toughness'] = 0

    return card
