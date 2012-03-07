from django.db import models


class SuperType(models.Model):
    name = models.CharField(max_length=9, unique=True)
    slug = models.SlugField(max_length=9)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']


class CardType(models.Model):
    name = models.CharField(max_length=12, unique=True)
    slug = models.SlugField(max_length=12)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']


class SubType(models.Model):
    name = models.CharField(max_length=24, unique=True)
    slug = models.SlugField(max_length=24)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']
