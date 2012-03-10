from django.template.defaultfilters import slugify
import re


def normalize(cards):
    """Normalize a bunch of cards' fields.
    """
    return [_normalize_card(card) for card in cards]


def _normalize_card(card):
    """Normalize a single card's fields.
    """
    card['name'] = re.sub('\s+', ' ', card['name'].lower().strip())
    card['slug'] = slugify(card['name'])
    return card
