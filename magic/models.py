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


class Card(models.Model):
    """A Magic: The Gathering card.
    """
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

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name
