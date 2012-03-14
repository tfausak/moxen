# pylint: disable=R0903,W0232
from django import forms
from django.db.models import Count, Q
import magic.models
import operator
import re


class ManaSymbolForm(forms.ModelForm):
    """Form for mana symbols.
    """
    class Meta:
        model = magic.models.ManaSymbol

    def clean_name(self):
        name = self.cleaned_data['name']
        name = name.lower()
        name = re.sub(r'\s', '', name)
        return name


class ManaCostForm(forms.ModelForm):
    """Form for mana costs.
    """
    class Meta:
        model = magic.models.ManaCost

    def clean_mana_symbols(self):
        mana_symbols = self.cleaned_data['mana_symbols']
        if (magic.models.ManaCost.objects
                .filter(reduce(operator.or_, (Q(mana_symbols=mana_symbol)
                    for mana_symbol in mana_symbols)))
                .annotate(count=Count('mana_symbols'))
                .filter(count=len(mana_symbols))):
            raise forms.ValidationError(
                'Mana cost with these Mana symbols already exists.')
        return mana_symbols


class UserProfileForm(forms.ModelForm):
    """Form for editing a user's profile.
    """
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)

    class Meta:
        exclude = ('user',)
        model = magic.models.UserProfile

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
