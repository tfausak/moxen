from django.db.transaction import commit_on_success
from magic.models import Card, PrintedCard


def store(data):
    """Store a bunch of cards.
    """
    with commit_on_success():
        cards = []
        for datum in data:
            cards.append(_store_card(datum))

    with commit_on_success():
        printed_cards = []
        for index, card in enumerate(cards):
            _store_printed_cards(card, data[index]['sets_rarities'])

    return printed_cards


def _store_card(data):
    """Store a single card.
    """
    card, _ = Card.objects.get_or_create(name=data['name'], slug=data['slug'])
    for key in ('rules_text', 'mana_cost', 'super_types', 'card_types',
            'sub_types', 'power', 'toughness', 'loyalty', 'hand_modifier',
            'life_modifier', 'colors', 'converted_mana_cost',
            'converted_power', 'converted_toughness'):
        setattr(card, key, data[key])
    card.save()
    return card


def _store_printed_cards(card, data):
    """Store a bunch of printed cards.
    """
    printed_cards = []
    for set_, rarity in data:
        printed_cards.append(_store_printed_card(card, set_, rarity))
    return printed_cards


def _store_printed_card(card, set_, rarity):
    """Store a single printed card.
    """
    printed_card, _ = PrintedCard.objects.get_or_create(card=card,
        set=set_, rarity=rarity)
    return printed_card
