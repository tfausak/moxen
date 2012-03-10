from magic.models import Card


def store(cards):
    """Store a bunch of cards.
    """
    return [_store_card(card) for card in cards]


def _store_card(card):
    """Store a single card.
    """
    card_, _ = Card.objects.get_or_create(name=card['name'], slug=card['slug'])
    card_.rules_text = card['rules_text']
    card_.save()
    return card_
