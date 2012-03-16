from collections import defaultdict
from magic.models import CardType, Color, Rarity, Set, SubType, SuperType
import re


GATHERER_URL = re.compile('^http://gatherer[.]wizards[.]com/')
GATHERER_TEXT_URL = re.compile(r'\bmethod=text\b')

# Every mana cost is made up of zero or more mana symbols.
MANA_SYMBOL = r'\d+|[wubrgxyzpstq]'
MANA_COST = re.compile(r'({0})|\(({0})/({0})\)'.format(MANA_SYMBOL))

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

# Every set in the database with a pre-computed regex for matching
# against a set-rarity pair.
SETS = []
for set_ in Set.objects.all():
    set_.pattern = re.compile('^{0} '.format(re.escape(set_.name)))
    SETS.append(set_)
SETS.sort(key=lambda set_: len(set_.name), reverse=True)

# Every rarity in the database with a pre-computed regex for matching
# against a set-rarity pair.
RARITIES = []
for rarity in Rarity.objects.all():
    rarity.pattern = re.compile(' {0}$'.format(re.escape(rarity.name)))
    RARITIES.append(rarity)
RARITIES.sort(key=lambda rarity: len(rarity.name), reverse=True)
