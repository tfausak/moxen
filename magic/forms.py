# pylint: disable=R0903,W0232
from django import forms
from django.db.models import Count, Q
from django.template.defaultfilters import slugify
import magic.models
import operator
import re


class ColorForm(forms.ModelForm):
    """Form for colors.
    """
    class Meta:
        model = magic.models.Color

    def clean_name(self):
        return re.sub(r'\s+', ' ', self.cleaned_data['name'].lower().strip())

    def clean_slug(self):
        slug = self.cleaned_data['slug']
        slug = slug.lower()
        return slug


class ManaSymbolForm(forms.ModelForm):
    """Form for mana symbols.
    """
    class Meta:
        model = magic.models.ManaSymbol

    def clean_name(self):
        return re.sub(r'\s+', '', self.cleaned_data['name'].lower())


class ManaCostForm(forms.ModelForm):
    """Form for mana costs.
    """
    class Meta:
        model = magic.models.ManaCost

    def clean_mana_symbols(self):
        mana_symbols = self.cleaned_data['mana_symbols']
        if (magic.models.ManaCost.objects
                .filter(reduce(operator.or_, (Q(mana_symbols=mana_symbol)
                    for mana_symbol in mana_symbols), Q()))
                .annotate(count=Count('mana_symbols'))
                .filter(count=len(mana_symbols))):
            raise forms.ValidationError(
                'Mana cost with these Mana symbols already exists.')
        return mana_symbols


class SuperTypeForm(forms.ModelForm):
    """Form for super types.
    """
    class Meta:
        model = magic.models.SuperType

    def clean_name(self):
        return re.sub(r'\s+', ' ', self.cleaned_data['name'].lower().strip())

    def clean_slug(self):
        return slugify(self.cleaned_data['name'])


class CardTypeForm(forms.ModelForm):
    """Form for card types.
    """
    class Meta:
        model = magic.models.CardType

    def clean_name(self):
        return re.sub(r'\s+', ' ', self.cleaned_data['name'].lower().strip())

    def clean_slug(self):
        return slugify(self.cleaned_data['name'])


class SubTypeForm(forms.ModelForm):
    """Form for sub types.
    """
    class Meta:
        model = magic.models.SubType

    def clean_name(self):
        return re.sub(r'\s+', ' ', self.cleaned_data['name'].lower().strip())

    def clean_slug(self):
        return slugify(self.cleaned_data['name'])


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
