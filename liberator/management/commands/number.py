from django.core.management.base import BaseCommand
from magic.models import Printing, Set


class Command(BaseCommand):
    def handle(self, *args, **options):
        slugs = ('1e', '2e', '2u', '3e', '4e', '5e', 'al', 'an', 'aq', 'bd',
            'br', 'ch', 'dk', 'fe', 'hm', 'ia', 'le', 'mi', 'p2', 'p4', 'po',
            'st', 'te', 'vi', 'wl')
        for slug in slugs:
            set_ = Set.objects.get(slug=slug)
            printings = list(Printing.objects.filter(set=set_))
            print set_, len(printings)

            printings.sort(key=lambda printing: printing.card.name)
            printings.sort(key=lambda printing: {
                'artifact': 1,
                'creature': 1,
                'enchantment': 1,
                'instant': 1,
                'land': 2,
                'plane': 1,
                'planeswalker': 1,
                'scheme': 1,
                'sorcery': 1,
                'tribal': 1,
                'vanguard': 1,
                'x': 1,
            }[getattr((printing.card.card_types.all() or [None])[0], 'name', 'x')])
            printings.sort(key=lambda printing: {
                'basic': 3,
                'legendary': 1,
                'ongoing': 1,
                'snow': 2,
                'world': 1,
                'x': 1,
            }[getattr((printing.card.super_types.all() or [None])[0], 'name', 'x')])
            printings.sort(key=lambda printing: {
                'w': 1,
                'u': 2,
                'b': 3,
                'r': 4,
                'g': 5,
                'x': 6,
            }[getattr((printing.card.colors.all() or [None])[0], 'slug', 'x')])

            number = 1
            for printing in printings:
                printing.number = number
                printing.save()
                number += 1

                print '', printing.number, printing
