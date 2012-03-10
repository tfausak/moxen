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
    card['mana_cost'] = '}{'.join('/'.join((x,) if x else (y, z))
        for x, y, z in card['mana_cost'])
    if card['mana_cost']:
        card['mana_cost'] = '{' + card['mana_cost'] + '}'

    return card
