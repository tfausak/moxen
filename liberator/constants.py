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

SUPER_TYPES = [(re.compile(r'\b{0}\b'.format(super_type.name)), super_type)
    for super_type in SuperType.objects.all()]
CARD_TYPES = [(re.compile(r'\b{0}\b'.format(card_type.name)), card_type)
    for card_type in CardType.objects.all()]
SUB_TYPES = [(re.compile(r'\b{0}\b'.format(sub_type.name)), sub_type)
    for sub_type in SubType.objects.all()]
COLORS = [(re.compile(r'\b{0}\b'.format(color.slug)), color)
    for color in Color.objects.all()]
