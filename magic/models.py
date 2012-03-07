from django.db import models


class SuperType(models.Model):
    name = models.CharField(max_length=9, unique=True)
    slug = models.SlugField(max_length=9, unique=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']


class CardType(models.Model):
    name = models.CharField(max_length=12, unique=True)
    slug = models.SlugField(max_length=12, unique=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']


class SubType(models.Model):
    name = models.CharField(max_length=24, unique=True)
    slug = models.SlugField(max_length=24, unique=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Set(models.Model):
    name = models.CharField(max_length=39, unique=True)
    slug = models.SlugField(max_length=3, unique=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Rarity(models.Model):
    name = models.CharField(max_length=11, unique=True)
    slug = models.SlugField(max_length=1, unique=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'rarities'
