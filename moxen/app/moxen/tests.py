# pylint: disable=R0904
from app.moxen.models import UserProfile
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase


class UserProfileTestCase(TestCase):
    def test_creates_user_profile(self):
        user = User()
        user.save()
        profile = UserProfile.objects.get(user=user)
        self.assertTrue(profile)


class DeleteUserTestCase(TestCase):
    def test_succeeds(self):
        user = User(username='will-be-deleted')
        user.set_password('-')
        user.save()
        self.client.login(username=user.username, password='-')
        self.client.get(reverse('delete_user'))
        user = User.objects.get(username='will-be-deleted')
        self.assertFalse(user.is_active)
