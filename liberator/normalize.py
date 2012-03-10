from django.template.defaultfilters import slugify
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

    return card
