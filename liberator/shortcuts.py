"""Shortcut functions to make liberating easier.
"""
from liberator.fetch import fetch
from liberator.parse import parse
from liberator.store import store
import logging


def liberate(url):
    """Free a card from the clutches of the web!
    """
    logging.info('Liberating <{0}>'.format(url))

    fetch_result = fetch(url)
    if fetch_result is None:
        logging.warning('Failed to fetch <{0}>'.format(url))
        return

    parse_result = parse(fetch_result)
    if parse_result is None:
        logging.warning('Failed to parse <{0}>'.format(url))

    store_result = store(parse_result)
    if store_result is None:
        logging.warning('Failed to store <{0}>'.format(url))

    return store_result
