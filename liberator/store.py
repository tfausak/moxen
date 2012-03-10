"""Functions to store cards from a web page into the database.
"""
from django.template.defaultfilters import slugify
from magic.models import CardAtom
import magic.constants


def store(data):
    """Save a bunch of cards.
    """
    card_atoms = []

    for datum in data:
        card_atom, _ = CardAtom.objects.get_or_create(name=datum['name'],
            slug=slugify(datum['name'].translate(
                magic.constants.CARD_SLUG_TRANSLATION_TABLE)))

        card_atom.rules_text = datum['rules_text']
        card_atom.save()

        card_atoms.append(card_atom)
    return card_atoms
