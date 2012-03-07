"""Update cards with information from the Gatherer.
"""
from BeautifulSoup import BeautifulSoup
from django.core.management.base import BaseCommand
from django.db import transaction
from urllib import quote
from urllib2 import urlopen
import magic.models
import re


class Command(BaseCommand):
    args = '[set set ...]'
    help = 'Update cards from the given sets.'

    def write(self, string, flush=False):
        """Shortcut for printing things if the verbosity is high enough.
        """
        if self.verbosity:
            self.stdout.write(string)
            if flush:
                self.stdout.flush()

    def normalize_card(self, card):
        """Switch from a list to a dict.

        Also performs some rudimentary normalization.
        """
        whitespace = re.compile(r'\s+')

        # Switch from positional to named.
        card = {
            'name': card[0].contents[3].contents[1],
            'mana_cost': card[1].contents[3],
            'type': card[2].contents[3],
            'misc': card[3].contents[3],
            'rules_text': card[4].contents[3],
            'set_rarity': card[5].contents[3],
        }

        # These fields are easy to normalize.
        for key in ('name', 'mana_cost', 'type', 'misc', 'set_rarity'):
            card[key] = card[key].string.strip().lower()
            card[key] = re.sub(whitespace, ' ', card[key])
            card[key] = re.sub(u'\u2019', "'", card[key])

        # The rules text is a little more complex.
        rules_text = ''
        for rule in card['rules_text']:
            if rule.string:
                rule = rule.string.strip()
                rule = re.sub(whitespace, ' ', rule)
                rules_text += rule + '\n'
        card['rules_text'] = rules_text.strip()

        return card

    def tokenize_mana_cost(self, mana_cost):
        """Convert a mana cost string into a list of string tokens.
        """
        # Find and remove all hybrid mana costs.
        hybrid = re.findall(self.hybrid_pattern, mana_cost)
        mana_cost = re.sub(self.hybrid_pattern, '', mana_cost)

        # Everthing else is just a regular mana cost.
        regular = re.findall(self.regular_pattern, mana_cost)
        return regular + hybrid

    def convert_mana_cost(self, mana_cost):
        """Calculate the converted mana cost of a tokenized mana cost.
        """
        converted_mana_cost = 0

        for token in mana_cost:
            # If it's not a string (unicode), it's a tuple of strings.
            if not isinstance(token, unicode):
                # The CMC of a hybrid is the max of the parts.
                converted_mana_cost += max([self.convert_mana_cost(x)
                    for x in token])
            else:
                # Add the int value, 1 (for wubrg), or 0 (for xyz).
                try:
                    converted_mana_cost += int(token)
                except ValueError:
                    converted_mana_cost += self.symbols.get(token, 0)

        return converted_mana_cost

    def stringify_mana_cost(self, mana_cost):
        """Convert a tokenized mana cost into a string.
        """
        # Convert hybrid tuples into /-separated strings.
        for index, token in enumerate(mana_cost):
            if not isinstance(token, str):
                mana_cost[index] = '/'.join(token)

        # Wrap everything in parentheses.
        if not mana_cost:
            return ''
        return '(' + ')('.join(mana_cost) + ')'

    def colors_from_mana_cost(self, mana_cost):
        """Figure out which colors are present in a mana cost.
        """
        return [color for color in self.colors if color.slug in mana_cost]

    def super_types_from_type(self, type_):
        """Determine a card's super types from its type.
        """
        types = []

        # We only care about the left side of the type line.
        type_ = type_.split(u'\u2014')[0].split()
        for super_type in self.super_types:
            if super_type.name in type_:
                types.append(super_type)

        return types

    def card_types_from_type(self, type_):
        """Determine a card's card type from its type.
        """
        types = []

        # We only care about the left side of the type line.
        type_ = type_.split(u'\u2014')[0].split()
        for card_type in self.card_types:
            if card_type.name in type_:
                types.append(card_type)

        return types

    def sub_types_from_type(self, type_):
        """Determine a card's sub type from its type.
        """
        types = []

        # We only care about the right side of the type line.
        type_ = type_.split(u'\u2014')
        type_ = type_[1].split() if len(type_) > 1 else []

        for sub_type in self.sub_types:
            # Some sub types have spaces in them.
            if ' ' in sub_type.name:
                append = sub_type.name in ' '.join(type_)
            else:
                append = sub_type.name in type_

            if append:
                types.append(sub_type)

        return types

    def resolve_misc(self, card):
        """Make sense of the "miscellaneous" field.

        It stands for power/toughness in creatures, loyalty in
        plainswalkers, or hand/life modifiers in Vanguard cards.
        """
        non_digit = re.compile('\D')

        # Set defaults.
        for key in ('power', 'toughness'):
            card[key] = ''
        for key in ('converted_power', 'converted_toughness', 'loyalty',
                'hand_modifier', 'life_modifier'):
            card[key] = 0

        # Pre-emptively grab P/T or H/L.
        matches = re.search(self.hybrid_pattern, card['misc'])
        if matches is None:
            left = right = '0'
        else:
            left, right = matches.groups('0')

        # Conditionally set stuff based on card type.
        if self.creature_type in card['card_types']:
            card['power'], card['toughness'] = left, right
            left = re.sub(non_digit, '', left) or 0
            right = re.sub(non_digit, '', right) or 0
            card['converted_power'] = int(left)
            card['converted_toughness'] = int(right)
        elif self.planeswalker_type in card['card_types']:
            card['loyalty'] = int(re.sub('\D', '', card['misc']) or 0)
        elif self.vanguard_type in card['card_types']:
            card['hand_modifier'] = int(left)
            card['life_modifier'] = int(right)

        del(card['misc'])

    def split_set_rarity(self, set_rarity):
        """Split a comma-separated string into a list of Set/Rarity objects.
        """
        sets_rarities = []

        for set_rarity in set_rarity.split(', '):
            for rarity in self.rarities:
                if re.search(rarity.re, set_rarity):
                    set_rarity = re.sub(rarity.re, '', set_rarity)
                    break
            for set in self.sets:
                if set.name == set_rarity:
                    break
            sets_rarities.append((set, rarity))

        return sets_rarities

    @transaction.commit_manually
    def handle(self, *args, **options):
        # Get everything set up to avoid DB calls and RE compiles.
        self.card_types = magic.models.CardType.objects.all()
        self.colors = magic.models.Color.objects.all()
        self.creature_type = magic.models.CardType.objects.get(name='creature')
        self.hybrid_pattern = re.compile(r'\((.+?)/(.+?)\)')
        self.planeswalker_type = magic.models.CardType.objects.get(
            name='planeswalker')
        self.rarities = magic.models.Rarity.objects.all()
        self.regular_pattern = re.compile(r'\d+|[wubrgxyz]')
        self.sets = magic.models.Set.objects.all()
        self.sub_types = magic.models.SubType.objects.all()
        self.super_types = magic.models.SuperType.objects.all()
        self.symbols = {'w': 1, 'u': 1, 'b': 1, 'r': 1, 'g': 1}
        self.vanguard_type = magic.models.CardType.objects.get(name='vanguard')
        self.verbosity = int(options['verbosity']) > 0

        # Build the Gatherer URL.
        url = 'http://gatherer.wizards.com/Pages/Search/Default.aspx' \
              '?method=text&output=spoiler&sort=abc+&special=true&set='
        if args:
            url += ''.join(['|["{0}"]'.format(quote(set)) for set in args])
        else:
            url += '|[]'
        self.write(url + '\n')

        # Open and parse the page.
        self.write('Opening...\n')
        page = urlopen(url)
        self.write('Parsing...\n')
        soup = BeautifulSoup(page)

        # Find cards.
        self.write('Finding cards...\n')
        tags = soup.find('div', attrs={'class': 'textspoiler'})
        tags = tags.findAll('tr')
        cards = []
        for index in range(0, len(tags), 7):
            cards.append(tags[index:index + 6])

        # Normalize cards.
        self.write('Normalizing...\n')
        for index, card in enumerate(cards):
            cards[index] = self.normalize_card(card)

        # Convert and calulcate mana cost.
        self.write('converted_mana_cost, mana_cost...\n')
        for card in cards:
            tokens = self.tokenize_mana_cost(card['mana_cost'])
            card['converted_mana_cost'] = self.convert_mana_cost(tokens)
            card['mana_cost'] = self.stringify_mana_cost(tokens)

        # Determine colors.
        self.write('colors...\n')
        for card in cards:
            card['colors'] = self.colors_from_mana_cost(card['mana_cost'])

        # Determine types.
        self.write('super_types, card_types, sub_types...\n')
        for card in cards:
            card['super_types'] = self.super_types_from_type(card['type'])
            card['card_types'] = self.card_types_from_type(card['type'])
            card['sub_types'] = self.sub_types_from_type(card['type'])
            del(card['type'])

        # Analyze miscellaneous field.
        self.write('misc...\n')
        for card in cards:
            card = self.resolve_misc(card)

        # Determine sets and rarities.
        self.write('set_rarity...\n')
        for rarity in self.rarities:
            rarity.re = re.compile(r' {0}$'.format(rarity.name))
        for card in cards:
            card['sets_rarities'] = self.split_set_rarity(
                card['set_rarity'])
            del(card['set_rarity'])

        # Find the card IDs.
        self.write('id...\n')
        for card in cards:
            try:
                card_db = magic.models.Card.objects.get(name=card['name'])
                card['id'] = card_db.id
                card_db.delete()
            except magic.models.Card.DoesNotExist:
                card['id'] = None
        transaction.commit()

        # Save the cards.
        self.write('Saving...\n')
        for card in cards:
            card['db'] = magic.models.Card(
                id=card['id'],
                name=card['name'],
                mana_cost=card['mana_cost'],
                power=card['power'],
                toughness=card['toughness'],
                rules_text=card['rules_text'],
                converted_mana_cost=card['converted_mana_cost'],
                converted_power=card['converted_power'],
                converted_toughness=card['converted_toughness'],
                loyalty=card['loyalty'],
                hand_modifier=card['hand_modifier'],
                life_modifier=card['life_modifier'],
            )
            card['db'].save()
            del(card['id'])
        transaction.commit()

        # Associate many-to-many fields.
        self.write('Associating many-to-many fields...\n')
        for card in cards:
            card['db'].super_types.add(*card['super_types'])
            card['db'].card_types.add(*card['card_types'])
            card['db'].sub_types.add(*card['sub_types'])
            card['db'].colors.add(*card['colors'])
            card['db'].save()
        transaction.commit()

        # Delete old instances.
        self.write('Deleting instances...\n')
        for card in cards:
            for instance in magic.models.CardInstance.objects.filter(
                    card=card['db']):
                instance.delete()
        transaction.commit()

        # Create new instances.
        self.write('Creating instances...\n')
        for card in cards:
            for set_rarity in card['sets_rarities']:
                card_instance = magic.models.CardInstance.objects.get_or_create(
                    card=card['db'],
                    set=set_rarity[0],
                    rarity=set_rarity[1]
                )
        transaction.commit()

        # And we're done!
        self.write('Done. {0} cards.\n'.format(len(cards)))
