from django import forms
from registration.forms import RegistrationFormUniqueEmail
import bauble.models


class UserProfileForm(forms.ModelForm):
    """Form for editing a user's profile.
    """
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)

    class Meta:
        exclude = ['user']
        model = bauble.models.UserProfile

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


class UserRegistrationForm(RegistrationFormUniqueEmail):
    def clean_username(self):
        blacklist = (
            'activate',
            'create',
            'edit',
            'login',
            'logout',
            'password',
            'register',
            'settings',
        )
        if self.cleaned_data['username'] in blacklist:
            raise forms.ValidationError(
                'This username is invalid. Please choose another.')

        return super(UserRegistrationForm, self).clean_username()
