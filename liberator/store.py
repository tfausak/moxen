"""Functions to store cards from a web page into the database.
"""


def store(cards):
    """Save a bunch of cards.
    """
    for card in cards:
        _store_card(card)


def _store_card(card):
    """Save a single card.
    """
    raise NotImplementedError
