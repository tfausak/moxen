"""Models for describing Magic: The Gathering cards.

Also includes models for describing associated metadata, like
printings and tournament restrictions.

References to the Magic: The Gathering comprehensive rules are
included where appropriate. <http://wizards.com/magic/rules>
"""
# pylint: disable=R0903,W0232
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Color(models.Model):
    """A color in Magic.

    The colors are defined and enumerated in 105.1.
    """
    name = models.CharField(max_length=5, unique=True)
    slug = models.SlugField(max_length=1, unique=True)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name


class ManaSymbol(models.Model):
    """A mana symbol.

    Mana symbols are enumerated in 107.4.
    """
    name = models.CharField(max_length=3, unique=True)
    colors = models.ManyToManyField(Color, blank=True)
    value = models.PositiveIntegerField(blank=True, default=0)

    class Meta:
        ordering = ['value', 'name']

    def __unicode__(self):
        return self.name


class ManaCost(models.Model):
    """A run of consecutive mana symbols.

    Used by the card model to specify a mana cost.
    """
    mana_symbol = models.ForeignKey(ManaSymbol)
    count = models.PositiveIntegerField(blank=True, default=1)

    class Meta:
        unique_together = ['mana_symbol', 'count']

    def __unicode__(self):
        return ' '.join(self.mana_symbol.name for _ in range(self.count))

    def mana_symbols(self):
        """Return a list of this mana cost's symbols.
        """
        return [self.mana_symbol] * self.count

    def value(self):
        """Calculate this mana cost's converted value.
        """
        return self.mana_symbol.value * self.count


class SuperType(models.Model):
    """A card's super type.

    Super types are defined in 205.4 and enumerated in 205.4a.
    """
    name = models.CharField(max_length=9, unique=True)
    slug = models.SlugField(max_length=9, unique=True)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name


class CardType(models.Model):
    """A card's card type.

    Card types are defined in 205.2 and enumerated in 205.2a.
    """
    name = models.CharField(max_length=12, unique=True)
    slug = models.SlugField(max_length=12, unique=True)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name


class SubType(models.Model):
    """A card's sub type.

    Sub types are defined in 205.3 and enumerated in 205.3g-p.
    """
    name = models.CharField(max_length=24, unique=True)
    slug = models.SlugField(max_length=24, unique=True)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name


class Set(models.Model):
    """A card's set, or expansion.

    Sets are defined in 206.1.
    """
    name = models.CharField(max_length=39, unique=True)
    slug = models.SlugField(max_length=3, unique=True)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name


class Rarity(models.Model):
    """A card's rarity.

    Rarities are defined and enumerated in 206.2.
    """
    name = models.CharField(max_length=11, unique=True)
    slug = models.SlugField(max_length=1, unique=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'rarities'

    def __unicode__(self):
        return self.name


class Card(models.Model):
    """A Magic: The Gathering card.

    The parts of a card are given in 200.1. Multi-card cards
    (double-faced, flip, and split) are explained in 711, 708, and
    709.
    """
    KIND_CHOICES = (
        ('n', 'normal'),
        ('d', 'double-faced'),
        ('f', 'flip'),
        ('s', 'split'),
    )

    # Every Magic card has a unique name (201.2). An elemental from
    # Unhinged has the longest name at 141 characters.
    name = models.CharField(max_length=141, unique=True)
    slug = models.SlugField(max_length=141, unique=True)

    # The rules text can be found in the text box (207.1).
    rules_text = models.TextField(blank=True)

    # Mana costs are usually at the top right (202.1).
    mana_cost = models.ManyToManyField(ManaCost, blank=True)

    # These are defined elsewhere, but they're all sourced from the
    # type line (205.1).
    super_types = models.ManyToManyField(SuperType, blank=True)
    card_types = models.ManyToManyField(CardType)
    sub_types = models.ManyToManyField(SubType, blank=True)

    # Creatures have power and toughness (208.1).
    power = models.CharField(blank=True, max_length=3)
    toughness = models.CharField(blank=True, max_length=3)
    converted_power = models.PositiveIntegerField(blank=True, default=0)
    converted_toughness = models.PositiveIntegerField(blank=True, default=0)

    # Planeswalkers have loyalty (209.1).
    loyalty = models.PositiveIntegerField(blank=True, default=0)

    # Vanguards have hand and life modifiers (210.1, 211.1).
    hand_modifier = models.IntegerField(blank=True, default=0)
    life_modifier = models.IntegerField(blank=True, default=0)

    # Some cards are comprised of more than one (conceptual) card
    # printed on one (actual) card.
    other_card = models.OneToOneField('self', blank=True, null=True)
    kind = models.CharField(choices=KIND_CHOICES, default=KIND_CHOICES[0][0],
        max_length=1)

    colors = models.ManyToManyField(Color, blank=True)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        if self.other_card:
            return u'{0} // {1} ({0})'.format(self.name, self.other_card.name)
        return self.name

    def save(self, *args, **kwargs):
        super(Card, self).save(*args, **kwargs)

        # Make the other relationship symmetric.
        if self.other_card is not None and (self.other_card.other_card != self
                or self.other_card.kind != self.kind):
            self.other_card.other_card = self
            self.other_card.kind = self.kind
            self.other_card.save()  # pylint: disable=E1101

    @models.permalink
    def get_absolute_url(self):
        return ('card_detail', (), {'slug': self.slug})

    def color(self):
        """Combine this card's colors.
        """
        colors = ' '.join(unicode(color) for color in self.colors.all())
        if self.colors.count() > 1:
            return 'multicolored ' + colors
        if self.colors.count():
            return 'monocolored ' + colors
        return 'colorless'

    def type(self):
        """Combine this card's super, card, and sub types.
        """
        super_types = ' '.join(unicode(super_type)
            for super_type in self.super_types.all())
        card_types = ' '.join(unicode(card_type)
            for card_type in self.card_types.all())
        sub_types = ' '.join(unicode(sub_type)
            for sub_type in self.sub_types.all())

        super_types += ' ' if super_types else ''
        card_types += ' \u2014 ' if sub_types else ''

        return super_types + card_types + sub_types

    def converted_mana_cost(self):
        """Calculate this card's converted mana cost.
        """
        return sum(mana_cost.value() for mana_cost in self.mana_cost.all())

    def mana_symbols(self):
        """Return this card's mana symbols in order.
        """
        mana_costs = []
        for mana_cost in self.mana_cost.all():
            if mana_cost.mana_symbol.name.isdigit():
                order = 2
            else:
                if mana_cost.mana_symbol.value == 0:
                    order = 1
                else:
                    if len(mana_cost.mana_symbol.name) > 1:
                        order = 3
                    else:
                        order = 4
            mana_costs.append((order, mana_cost))
        mana_costs.sort(key=lambda item: item[1].mana_symbol.name)
        mana_costs.sort(key=lambda item: item[0])
        return [mana_cost.mana_symbols() for order, mana_cost in mana_costs]


class Printing(models.Model):
    """A printed card.

    One card can (and often is) printed in multiple sets. Within
    each set, its rarity might be different than any other.
    """
    card = models.ForeignKey(Card)
    set = models.ForeignKey(Set)
    rarity = models.ForeignKey(Rarity)

    class Meta:
        ordering = ['card__name']
        unique_together = ['card', 'set', 'rarity']

    def __unicode__(self):
        return u'{0} ({1} {2})'.format(self.card, self.set, self.rarity)


class Block(models.Model):
    """A collection of sets.

    Each block is usually comprised of three sets, one significantly
    larger than the other two.
    """
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    sets = models.ManyToManyField(Set)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name


class Format(models.Model):
    """A way to play Magic, with card restrictions.

    Formats define a way to play Magic. They limit the available
    sets and cards. They also enforce rules for deck construction
    and gameplay.
    """
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(blank=True, max_length=255, unique=True)
    sets = models.ManyToManyField(Set)
    cards = models.ManyToManyField(Card, blank=True, through='Legality')

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name


class Legality(models.Model):
    """A card's legality status within a format.

    A card can be banned (not allowed at all) or restricted (only
    one copy allowed).
    """
    STATUS_CHOICES = (
        ('b', 'banned'),
        ('r', 'restricted'),
    )

    card = models.ForeignKey(Card)
    format = models.ForeignKey(Format)
    status = models.CharField(choices=STATUS_CHOICES, max_length=1)

    class Meta:
        ordering = ['card__name']
        verbose_name_plural = 'legalities'

    def __unicode__(self):
        return u'{0} ({1} in {2})'.format(self.card,
            dict(self.STATUS_CHOICES)[self.status], self.format)


class UserProfile(models.Model):
    """Extra information about a user.
    """
    # pylint: disable=E1101
    user = models.OneToOneField(User, related_name='profile')

    def __unicode__(self):
        return self.user.get_full_name() or self.user.username

    @models.permalink
    def get_absolute_url(self):
        return ('profiles_profile_detail', (),
            {'username': self.user.username})


@receiver(post_save, sender=User)
def create_user_profile(instance=None, created=False, **_):
    """Create a user profile for new users.
    """
    if created:
        UserProfile(user=instance).save()
