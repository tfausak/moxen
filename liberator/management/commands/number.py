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
    colors = ''.join(sorted(
        color.slug for color in printing.card.colors.all()))

    # Colorless
    if colors == '':
        result = 22

    # Monocolored
    elif colors == 'w':
        result = 1
    elif colors == 'u':
        result = 2
    elif colors == 'b':
        result = 3
    elif colors == 'r':
        result = 4
    elif colors == 'g':
        result = 5

    # Multicolored (2 colors)
    elif colors == 'uw':
        result = 6
    elif colors == 'bu':
        result = 7
    elif colors == 'br':
        result = 8
    elif colors == 'gr':
        result = 9
    elif colors == 'gw':
        result = 10
    elif colors == 'bw':
        result = 11
    elif colors == 'ru':
        result = 12
    elif colors == 'bg':
        result = 13
    elif colors == 'rw':
        result = 14
    elif colors == 'gu':
        result = 15

    # Multicolored (3 colors)
    elif colors == 'buw':
        result = 16
    elif colors == 'bru':
        result = 17
    elif colors == 'bgr':
        result = 18
    elif colors == 'grw':
        result = 19
    elif colors == 'guw':
        result = 20

    # Multicolored (4+ colors)
    else:
        result = 21

    return result


def sort_by_land(printing):
    is_land = any(
        type_.name == 'land' for type_ in printing.card.card_types.all())
    if is_land:
        result = None

        # Snow-covered basic lands
        if printing.card.name == 'snow-covered plains':
            result = 2
        elif printing.card.name == 'snow-covered island':
            result = 3
        elif printing.card.name == 'snow-covered swamp':
            result = 4
        elif printing.card.name == 'snow-covered mountain':
            result = 5
        elif printing.card.name == 'snow-covered forest':
            result = 6

        # Basic lands
        elif printing.card.name == 'plains':
            result = 7
        elif printing.card.name == 'island':
            result = 8
        elif printing.card.name == 'swamp':
            result = 9
        elif printing.card.name == 'mountain':
            result = 10
        elif printing.card.name == 'forest':
            result = 11

        if result is not None:
            return result
    return is_land
