from collections import defaultdict
from magic.models import CardType, Color, SubType, SuperType
import re


GATHERER_URL = re.compile('^http://gatherer[.]wizards[.]com/')
GATHERER_TEXT_URL = re.compile(r'\bmethod=text\b')

MANA_SYMBOL = r'\d+|[wubrgxyz]'
MANA_COST = defaultdict(lambda: 0, {
    'w': 1, 'u': 1, 'b': 1, 'r': 1, 'g': 1,
    '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
    '10': 10, '11': 11, '12': 12, '13': 13, '14': 14, '15': 15, '16': 16,
})

# Card normalization depends on knowing which type the card is.
CREATURE_CARD_TYPE = CardType.objects.get(name='creature')
PLANESWALKER_CARD_TYPE = CardType.objects.get(name='planeswalker')
VANGUARD_CARD_TYPE = CardType.objects.get(name='vanguard')

# Every super type in the database with a pre-computed regex for
# matching against the type line.
SUPER_TYPES = []
for super_type in SuperType.objects.all():
    super_type.pattern = re.compile(
        r'\b{0}\b'.format(re.escape(super_type.name)))
    SUPER_TYPES.append(super_type)

# Every card type in the database with a pre-computed regex for matching
# against the type line.
CARD_TYPES = []
for card_type in CardType.objects.all():
    card_type.pattern = re.compile(
        r'\b{0}\b'.format(re.escape(card_type.name)))
    CARD_TYPES.append(card_type)

# Every sub type in the database with a pre-computed regex for matching
# against the type line.
SUB_TYPES = []
for sub_type in SubType.objects.all():
    sub_type.pattern = re.compile(
        r'\b{0}\b'.format(re.escape(sub_type.name)))
    SUB_TYPES.append(sub_type)

# Every color in the database with a pre-computed regex for matching
# against the mana cost.
COLORS = []
for color in Color.objects.all():
    color.pattern = re.compile(r'\b{0}\b'.format(re.escape(color.slug)))
    COLORS.append(color)
