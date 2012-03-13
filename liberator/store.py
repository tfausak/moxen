from django.db.transaction import commit_on_success
from magic.models import Card, Printing


def store(data):
    """Store a bunch of cards.
    """
    with commit_on_success():
        cards = []
        for datum in data:
            cards.append(_store_card(datum))

    with commit_on_success():
        printings = []
        for index, card in enumerate(cards):
            _store_printings(card, data[index]['sets_rarities'])

    return printings


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


def _store_printings(card, data):
    """Store a bunch of printing.
    """
    printings = []
    for set_, rarity in data:
        printings.append(_store_printing(card, set_, rarity))
    return printings


def _store_printing(card, set_, rarity):
    """Store a single printing.
    """
    printing, _ = Printing.objects.get_or_create(card=card,
        set=set_, rarity=rarity)
    return printing
