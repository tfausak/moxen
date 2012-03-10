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

    # Split the page into sections that describe cards.
    tags = dom.find('div', 'textspoiler').findAll('tr')
    cards = [tags[index:index + 6] for index in range(0, len(tags), 7)]

    # Extract card information from the DOM.
    for index, card in enumerate(cards):
        cards[index] = {
            'name': card[0].contents[3].contents[1].string,
            'rules_text': card[4].contents[3].findAll(text=True),
        }
    return cards
