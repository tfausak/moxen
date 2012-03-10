import re


GATHERER_URL = re.compile('^http://gatherer[.]wizards[.]com/')
GATHERER_TEXT_URL = re.compile(r'\bmethod=text\b')

MANA_SYMBOL = r'\d+|[wubrgxyz]'
