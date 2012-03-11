"""Functions for extracting card information from web pages.
"""
from BeautifulSoup import BeautifulSoup
import liberator.constants
import re


def parse(response):
    """Parse a web page.
    """
    function = None
    if re.search(liberator.constants.GATHERER_URL, response.geturl()):
        function = _parse_gatherer

    if function is not None:
        return function(response)


def _parse_gatherer(response):
    """Parse a page from the Gatherer.
    """
    function = None
    if re.search(liberator.constants.GATHERER_TEXT_URL, response.geturl()):
        function = _parse_gatherer_text

    if function is not None:
        return function(response)


def _parse_gatherer_text(response):
    """Parse a page of text spoilers from the Gatherer.
    """
    dom = BeautifulSoup(response)
    tags = dom.findAll('a', 'nameLink')
    cards = []
    for tag in tags:
        tag = tag.parent.parent
        card = [tag] + tag.findNextSiblings('tr', limit=6)
        if card[1].contents[3].string.lower().strip() == 'vanguard':
            # Vanguard cards are missing the "Cost:" line.
            cards.append({
                'color': '',
                'mana_cost': '',
                'misc': card[2].contents[3].string,
                'name': card[0].contents[3].contents[1].string,
                'rules_text': card[3].contents[3].findAll(text=True),
                'sets_rarities': card[4].contents[3].string,
                'type': card[1].contents[3].string,
            })
        elif card[2].contents[1].string.lower().strip() == 'color:':
            # Cards without a mana cost have a "Color:" line.
            cards.append({
                'color': card[2].contents[3].string,
                'mana_cost': card[1].contents[3].string,
                'misc': card[4].contents[3].string,
                'name': card[0].contents[3].contents[1].string,
                'rules_text': card[5].contents[3].findAll(text=True),
                'sets_rarities': card[6].contents[3].string,
                'type': card[3].contents[3].string,
            })
        else:
            cards.append({
                'color': '',
                'mana_cost': card[1].contents[3].string,
                'misc': card[3].contents[3].string,
                'name': card[0].contents[3].contents[1].string,
                'rules_text': card[4].contents[3].findAll(text=True),
                'sets_rarities': card[5].contents[3].string,
                'type': card[2].contents[3].string,
            })
    return cards
