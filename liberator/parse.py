"""Functions to parse web pages.
"""
from BeautifulSoup import BeautifulSoup
import liberator.constants
import re


def parse(response):
    """Parse a web page.
    """
    function = None
    url = response.geturl()
    if re.match(liberator.constants.GATHERER_URL, url):
        function = _parse_gatherer

    if function is not None:
        return function(response)


def _parse_gatherer(response):
    """Parse a page from the Gatherer.
    """
    function = None
    url = response.geturl()
    if re.search(liberator.constants.GATHERER_STANDARD_URL, url):
        function = _parse_gatherer_standard
    elif re.search(liberator.constants.GATHERER_COMPACT_URL, url):
        function = _parse_gatherer_compact
    elif re.search(liberator.constants.GATHERER_CHECKLIST_URL, url):
        function = _parse_gatherer_checklist
    elif re.search(liberator.constants.GATHERER_VISUAL_URL, url):
        function = _parse_gatherer_visual
    elif re.search(liberator.constants.GATHERER_TEXT_URL, url):
        function = _parse_gatherer_text
    elif re.search(liberator.constants.GATHERER_CARD_URL, url):
        function = _parse_gatherer_card

    if function is not None:
        return function(response)


def _parse_gatherer_standard(response):
    """Parse a listing of cards from the Gatherer in the standard format.
    """
    raise NotImplementedError


def _parse_gatherer_compact(response):
    """Parse a listing of cards from the Gatherer in the compact format.
    """
    raise NotImplementedError


def _parse_gatherer_checklist(response):
    """Parse a listing of cards from the Gatherer in the checklist format.
    """
    raise NotImplementedError


def _parse_gatherer_visual(response):
    """Parse a listing of cards from the Gatherer in the visual format.
    """
    raise NotImplementedError


def _parse_gatherer_text(response):
    """Parse a listing of cards from the Gatherer in the text format.
    """
    dom = BeautifulSoup(response)

    # Split the page into sections that describe cards.
    tags = dom.find('div', 'textspoiler').findAll('tr')
    cards = [tags[index:index + 6] for index in range(0, len(tags), 7)]

    for index, card in enumerate(cards):
        # Extract data from the DOM into a dictionary.
        card = {
            'name': card[0].contents[3].contents[1],
            'mana_cost': card[1].contents[3],
            'type': card[2].contents[3],
            'misc': card[3].contents[3],
            'rules_text': card[4].contents[3],
            'set_rarity': card[5].contents[3],
        }

        # Normalize fields.
        for key in ('name', 'mana_cost', 'type', 'misc', 'set_rarity'):
            card[key] = card[key].string.lower().strip()
            card[key] = re.sub(r'\s\+', ' ', card[key])
            card[key] = re.sub(u'\u2019', '\'', card[key])
        card['rules_text'] = ''.join(card['rules_text'].findAll(text=True))
        card['rules_text'] = card['rules_text'].strip()
        card['rules_text'] = re.sub(r'\s\+', ' ', card['rules_text'])

        cards[index] = card

    return cards


def _parse_gatherer_card(response):
    """Parse a single card from the Gatherer.
    """
    raise NotImplementedError
