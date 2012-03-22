from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    """Extra information about a user.
    """  # pylint: disable=E1101
    user = models.OneToOneField(User, related_name='profile')

    def __unicode__(self):
        return self.user.username

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
