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
        # Extract card information from the DOM.
        card = {
            'mana_cost': card[1].contents[3],
            'name': card[0].contents[3].contents[1],
            'rules_text': card[4].contents[3],
        }

        # Normalize card information.
        for key in ('mana_cost', 'name'):
            card[key] = card[key].string.lower().strip()

        # Get the card's canonical name.
        match = re.match('^(.*) \((.*)\)$', card['name'])
        if match:
            card['name'] = match.group(2)

        # Compile rules text.
        card['rules_text'] = '\n'.join(string.strip()
            for string in card['rules_text'].findAll(text=True))

        # Split mana cost into tokens.
        card['mana_cost'] = re.findall(r'\d+|[wubrgxyz]',
            re.sub(r'\((.+?)/(.+?)\)', '', card['mana_cost'])) + re.findall(
                r'\((.+?)/(.+?)\)', card['mana_cost'])

        cards[index] = card

    return cards


def _parse_gatherer_card(response):
    """Parse a single card from the Gatherer.
    """
    raise NotImplementedError
