from collections import defaultdict
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db.models import Q
from magic.models import Card, Deck, DeckCard
import logging
import random
import re
import string
import sys


def import_deck(decklist):
    cards = defaultdict(lambda: [0, 0])
    sideboard = False
    comment_pattern = re.compile(r'\s*#(.*)$')
    number_pattern = re.compile(r'^\s*(\d+).?\s+')

    for line in decklist.split('\n'):
        line = re.sub(r'\s+', ' ', line.lower().strip())

        # Strip comments.
        match = re.search(comment_pattern, line)
        comment = None
        if match:
            comment = match.group(1).strip()
            line = re.sub(comment_pattern, '', line)

        # Detect switch to sideboard listing.
        if comment == 'sideboard':
            sideboard = True

        # Skip empty lines.
        if not line:
            continue

        # Determine the number of cards.
        match = re.search(number_pattern, line)
        if match:
            number = int(match.group(1))
            line = re.sub(number_pattern, '', line)
        else:
            number = 1

        # Figure out which card it is.
        try:
            card = Card.objects.get(
                Q(ascii_name__iexact=line) | Q(name__iexact=line))
        except Card.DoesNotExist:
            logging.debug(u'Unknown card: %s', line)
            continue

        # Tally this card.
        cards[card][sideboard] += number

    deck = Deck(user=User.objects.all()[0],
        name='test-deck-{0}'.format(
            ''.join(random.choice(string.lowercase) for _ in range(5))))
    deck.save()
    for card, counts in cards.items():
        for sideboard, number in enumerate(counts):
            if number:
                deck_card = DeckCard(deck=deck, number=number, card=card,
                    sideboard=sideboard)
                deck_card.save()

    return deck


def export_deck(deck):
    decklist = u'# {0}\n'.format(deck)
    decklist += u'# by {0}\n'.format(deck.user)
    decklist += '\n'

    sideboard = False
    for deck_card in DeckCard.objects.filter(deck=deck):
        if not sideboard and deck_card.sideboard:
            decklist += '\n'
            decklist += '# Sideboard\n'
            sideboard = True

        decklist += u'{0} {1}\n'.format(deck_card.number, deck_card.card)

    return decklist


class Command(BaseCommand):
    def handle(self, *args, **options):
        print export_deck(import_deck(sys.stdin.read()))
