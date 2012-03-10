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
        card = [tag] + tag.findNextSiblings('tr', limit=5)
        cards.append({
            'name': card[0].contents[3].contents[1].string,
            'rules_text': card[4].contents[3].findAll(text=True),
            'mana_cost': card[1].contents[3].string,
            'type': card[2].contents[3].string,
            'misc': card[3].contents[3].string,
        })
    return cards
