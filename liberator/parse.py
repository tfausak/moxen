"""Functions to parse web pages.
"""
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
    raise NotImplementedError


def _parse_gatherer_card(response):
    """Parse a single card from the Gatherer.
    """
    raise NotImplementedError
