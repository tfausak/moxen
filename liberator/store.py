from magic.models import Card


def store(cards):
    """Store a bunch of cards.
    """
    return [_store_card(card) for card in cards]


def _store_card(card):
    """Store a single card.
    """
    card, _ = Card.objects.get_or_create(**card)
    return card
