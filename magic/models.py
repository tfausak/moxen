from django.db import models


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

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name
