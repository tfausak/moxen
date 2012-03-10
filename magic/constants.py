# Django's built-in slugify function doesn't handle these Unicode
# characters properly.
CARD_SLUG_TRANSLATION_TABLE = {
    174: 'r',
    230: 'ae',
}

LEGALITY_STATUS_CHOICES = (
    ('b', 'banned'),
    ('r', 'restricted'),
)
