from django.db import models


class Card(models.Model):
    """A Magic: The Gathering card.
    """
    # Every Magic card has a unique name (201.2). An elemental from
    # Unhinged has the longest name at 141 characters.
    name = models.CharField(max_length=141, unique=True)
    slug = models.SlugField(max_length=141, unique=True)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name
