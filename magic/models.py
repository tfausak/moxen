from django.db import models


class SuperType(models.Model):
    """Super type (205.4a).
    """
    name = models.CharField(max_length=9, unique=True)
    slug = models.SlugField(max_length=9, unique=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']


class CardType(models.Model):
    """Card type (205.2a).
    """
    name = models.CharField(max_length=12, unique=True)
    slug = models.SlugField(max_length=12, unique=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']


class SubType(models.Model):
    """Sub type (205.3g-p).
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
    """A Magic: The Gathering card.
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

    # Mana costs are usually at the top right (202.1). There are a
    # bunch of cards with five hybrid symbols, each of which takes
    # five characters.
    mana_cost = models.CharField(blank=True, max_length=25)

    # These are defined elsewhere, but they're all sourced from the
    # type line (205.1).
    super_types = models.ManyToManyField(SuperType, blank=True)
    card_types = models.ManyToManyField(CardType)
    sub_types = models.ManyToManyField(SubType, blank=True)

    # Creatures have power and toughness (208.1), planeswalkers
    # have loyalty (209.1), and vangaurds have modifiers (210.1,
    # 211.1).
    power = models.CharField(blank=True, max_length=3)
    toughness = models.CharField(blank=True, max_length=3)
    loyalty = models.PositiveIntegerField(blank=True, default=0)
    hand_modifier = models.IntegerField(blank=True, default=0)
    life_modifier = models.IntegerField(blank=True, default=0)

    # Some cards are comprised of more than one (conceptual) card
    # printed on one (actual) card.
    other = models.OneToOneField('self', blank=True, null=True)
    kind = models.CharField(blank=True, choices=KIND_CHOICES,
        default=KIND_CHOICES[0][0], max_length=1)

    # These fields are derived from other fields.
    colors = models.ManyToManyField(Color, blank=True)
    converted_mana_cost = models.PositiveIntegerField(blank=True, default=0)
    converted_power = models.PositiveIntegerField(blank=True, default=0)
    converted_toughness = models.PositiveIntegerField(blank=True, default=0)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name
