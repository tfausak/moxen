"""Functions to get web pages.
"""
from urllib2 import urlopen
import liberator.constants
import re


def fetch(url):
    """Get a web page.
    """
    function = None
    if re.match(liberator.constants.GATHERER_URL, url):
        function = _fetch_gatherer

    if function is not None:
        return function(url)


def _fetch_gatherer(url):
    """Get a page from the Gatherer.
    """
    return urlopen(url)
