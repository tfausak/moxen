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

            printings.sort(key=sort_by_name)
            printings.sort(key=sort_by_color)
            printings.sort(key=sort_by_land)

            number = 1
            for printing in printings:
                if number != printing.number:
                    print u' {0:3d} {1}'.format(number, printing.card.name)
                    printing.number = number
                    printing.save()
                number += 1


def sort_by_name(printing):
    return (printing.card.name.lower()
        .replace(u'\xe0', 'a')
        .replace(u'\xe1', 'a')
        .replace(u'\xe2', 'a')
        .replace(u'\xe6', 'ae')
        .replace(u'\xe9', 'e')
        .replace(u'\xed', 'i')
        .replace(u'\xf6', 'o')
        .replace(u'\xfa', 'u')
        .replace(u'\xfb', 'u'))


def sort_by_color(printing):
    colors = ''.join(sorted(color.slug for color in printing.card.colors.all()))

    # Colorless
    if colors == '': return 22

    # Monocolored
    if colors == 'w': return 1
    if colors == 'u': return 2
    if colors == 'b': return 3
    if colors == 'r': return 4
    if colors == 'g': return 5

    # Multicolored (2 colors)
    if colors == 'uw': return 6
    if colors == 'bu': return 7
    if colors == 'br': return 8
    if colors == 'gr': return 9
    if colors == 'gw': return 10
    if colors == 'bw': return 11
    if colors == 'ru': return 12
    if colors == 'bg': return 13
    if colors == 'rw': return 14
    if colors == 'gu': return 15

    # Multicolored (3 colors)
    if colors == 'buw': return 16
    if colors == 'bru': return 17
    if colors == 'bgr': return 18
    if colors == 'grw': return 19
    if colors == 'guw': return 20

    return 21


def sort_by_land(printing):
    is_land = any(
        type_.name == 'land' for type_ in printing.card.card_types.all())
    if is_land:
        if printing.card.name == 'plains':
            return 2
        elif printing.card.name == 'island':
            return 3
        elif printing.card.name == 'swamp':
            return 4
        elif printing.card.name == 'mountain':
            return 5
        elif printing.card.name == 'forest':
            return 6
    return is_land
