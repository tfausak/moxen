"""Shortcut functions to make liberating easier.
"""
from liberator.fetch import fetch
from liberator.parse import parse
from liberator.store import store


def liberate(url):
    """Free a card from the clutches of the web!
    """
    return store(parse(fetch(url)))
