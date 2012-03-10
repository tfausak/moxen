from collections import defaultdict


# Django's built-in slugify function doesn't handle these Unicode
# characters properly.
CARD_SLUG_TRANSLATION_TABLE = {
    174: 'r',
    230: 'ae',
}

# Mana symbols have a converted value, which an integer. For ease
# of use, every non-zero value is enumerated here.
CONVERTED_MANA_COST = defaultdict(lambda: 0, {
    'w': 1, 'u': 1, 'b': 1, 'r': 1, 'g': 1,
    '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
    '10': 10, '11': 11, '12': 12, '13': 13, '14': 14, '15': 15, '16': 16,
})

LEGALITY_STATUS_CHOICES = (
    ('b', 'banned'),
    ('r', 'restricted'),
)
