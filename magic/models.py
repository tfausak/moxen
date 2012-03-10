"""Models for Magic: The Gathering cards.

Cryptic numbers and letters probably refer to the comprehensive rules:
http://www.wizards.com/magic/comprules/MagicCompRules_20120201.txt
"""
from django.db import models
import magic.constants


class SuperType(models.Model):
    """Super type (205.4).
    """
    name = models.CharField(max_length=9, unique=True)
    slug = models.SlugField(max_length=9, unique=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']


class CardType(models.Model):
    """Card type (205.2).
    """
    name = models.CharField(max_length=12, unique=True)
    slug = models.SlugField(max_length=12, unique=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']


class SubType(models.Model):
    """Sub type (205.3).
    """
    name = models.CharField(max_length=24, unique=True)
    slug = models.SlugField(max_length=24, unique=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Set(models.Model):
    """Set (206.1).
    """
    name = models.CharField(max_length=39, unique=True)
    slug = models.SlugField(max_length=3, unique=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Rarity(models.Model):
    """Rarity (206.2).
    """
    name = models.CharField(max_length=11, unique=True)
    slug = models.SlugField(max_length=1, unique=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'rarities'


class Color(models.Model):
    """Color (105.1).
    """
    name = models.CharField(max_length=5, unique=True)
    slug = models.SlugField(max_length=1, unique=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Card(models.Model):
    """What you think of when you hear the word "card".
    """
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    kind = models.CharField(choices=magic.constants.CARD_KIND_CHOICES,
        default=magic.constants.CARD_KIND_CHOICES[0][0], max_length=1)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']


class CardAtom(models.Model):
    """Card (200.1).
    """
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    card = models.ForeignKey(Card, blank=True, null=True,
        related_name='card_atoms')

    mana_cost = models.CharField(blank=True, max_length=255)
    power = models.CharField(blank=True, max_length=255)
    toughness = models.CharField(blank=True, max_length=255)
    rules_text = models.TextField(blank=True)

    super_types = models.ManyToManyField(SuperType, blank=True)
    card_types = models.ManyToManyField(CardType)
    sub_types = models.ManyToManyField(SubType, blank=True)
    colors = models.ManyToManyField(Color, blank=True)

    converted_mana_cost = models.PositiveIntegerField(default=0)
    converted_power = models.PositiveIntegerField(default=0)
    converted_toughness = models.PositiveIntegerField(default=0)
    loyalty = models.PositiveIntegerField(default=0)
    hand_modifier = models.IntegerField(default=0)
    life_modifier = models.IntegerField(default=0)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Block(models.Model):
    """A group of sets, usually three.
    """
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    sets = models.ManyToManyField(Set)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Format(models.Model):
    """A DCI-sanctioned tournament format.
    """
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    sets = models.ManyToManyField(Set)
    cards = models.ManyToManyField(Card, through='Legality')

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Legality(models.Model):
    """The legality of a card within a format.
    """
    card = models.ForeignKey(Card)
    format = models.ForeignKey(Format)
    status = models.CharField(choices=magic.constants.LEGALITY_STATUS_CHOICES,
        max_length=1)

    class Meta:
        verbose_name_plural = 'legalities'
