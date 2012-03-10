from magic.models import Card


def store(cards):
    """Store a bunch of cards.
    """
    return [_store_card(card) for card in cards]


def _store_card(card):
    """Store a single card.
    """
    card_, _ = Card.objects.get_or_create(name=card['name'], slug=card['slug'])
    for key in ('rules_text', 'mana_cost', 'super_types', 'card_types',
            'sub_types', 'power', 'toughness', 'loyalty', 'hand_modifier',
            'life_modifier', 'colors', 'converted_mana_cost',
            'converted_power', 'converted_toughness'):
        setattr(card_, key, card[key])
    card_.save()
    return card_
