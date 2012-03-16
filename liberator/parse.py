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
    card, cards = {}, []
    for row in dom.find('div', 'textspoiler').findAll('tr'):
        cells = row.findAll('td')
        if len(cells) != 1:
            key = re.sub('[^a-z]', '_', cells[0].string.strip().lower()[:-1])
            value = '\n'.join(text for text in cells[1].findAll(text=True))
            card[key] = value
        else:
            cards.append(card)
            card = {}
    return cards
