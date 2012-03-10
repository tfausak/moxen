from liberator.fetch import fetch
from liberator.parse import parse
from liberator.normalize import normalize
from liberator.store import store


def liberate(url):
    """A shortcut for liberating a card's web page.
    """
    return store(normalize(parse(fetch(url))))
