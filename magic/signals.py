"""Django signal receivers.
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from magic.models import User, UserProfile


@receiver(post_save, sender=User)
def create_user_profile(instance=None, created=False, **kwargs):
    """Create a user profile for new users.
    """
    if created:
        UserProfile(user=instance).save()
