from django.db import models


class Card(models.Model):
    """A Magic: The Gathering card.
    """
    name = models.CharField(max_length=141, unique=True)
    slug = models.SlugField(max_length=141, unique=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']
