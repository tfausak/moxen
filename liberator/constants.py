from magic.models import CardType, SubType, SuperType
import re


GATHERER_URL = re.compile('^http://gatherer[.]wizards[.]com/')
GATHERER_TEXT_URL = re.compile(r'\bmethod=text\b')

MANA_SYMBOL = r'\d+|[wubrgxyz]'

SUPER_TYPES = [(re.compile(r'\b{0}\b'.format(super_type.name)), super_type)
    for super_type in SuperType.objects.all()]
CARD_TYPES = [(re.compile(r'\b{0}\b'.format(card_type.name)), card_type)
    for card_type in CardType.objects.all()]
SUB_TYPES = [(re.compile(r'\b{0}\b'.format(sub_type.name)), sub_type)
    for sub_type in SubType.objects.all()]
