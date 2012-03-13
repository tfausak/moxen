# pylint: disable=R0903,W0232
from django import forms
from magic.models import UserProfile


class UserProfileForm(forms.ModelForm):
    """Form for editing a user's profile.
    """
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)

    class Meta:
        exclude = ('user',)
        model = UserProfile

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].initial = self.instance.user.first_name
        self.fields['last_name'].initial = self.instance.user.last_name

    def save(self, *args, **kwargs):
        user = self.instance.user
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        return super(UserProfileForm, self).save(*args, **kwargs)
