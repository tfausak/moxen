from django.db import models


class SuperType(models.Model):
    name = models.CharField(max_length=9, unique=True)
    slug = models.SlugField(max_length=9)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']
