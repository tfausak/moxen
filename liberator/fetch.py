"""Functions for getting web pages.
"""
from urllib2 import urlopen
import liberator.constants
import re


def fetch(url):
    """Fetch a web page.
    """
    function = None
    if re.search(liberator.constants.GATHERER_URL, url):
        function = _fetch_gatherer

    if function is not None:
        return function(url)


def _fetch_gatherer(url):
    """Fetch a page from the Gatherer.
    """
    return urlopen(url)
