# pylint: disable=R0903,W0232
from django import forms
from django.template.defaultfilters import slugify
import magic.models
import re


class ColorForm(forms.ModelForm):
    """Form for colors.
    """
    class Meta:
        model = magic.models.Color

    def clean_name(self):
        return re.sub(r'\s+', ' ', self.cleaned_data['name'].lower().strip())

    def clean_slug(self):
        return re.sub(r'\s+', '', self.cleaned_data['slug'].lower())


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

    def clean_count(self):
        count = self.cleaned_data['count']
        if count < 1:
            raise forms.ValidationError(
                'Ensure this value is greater than or equal to 1.')
        return count


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


class SetForm(forms.ModelForm):
    """Form for sets.
    """
    class Meta:
        model = magic.models.Set

    def clean_name(self):
        return re.sub(r'\s+', ' ', self.cleaned_data['name'].lower().strip())

    def clean_slug(self):
        return re.sub(r'\s+', '', self.cleaned_data['slug'].lower())


class RarityForm(forms.ModelForm):
    """Form for rarities.
    """
    class Meta:
        model = magic.models.Rarity

    def clean_name(self):
        return re.sub(r'\s+', ' ', self.cleaned_data['name'].lower().strip())

    def clean_slug(self):
        return re.sub(r'\s+', '', self.cleaned_data['slug'].lower())


class CardForm(forms.ModelForm):
    """Form for cards.
    """
    class Meta:
        model = magic.models.Card

    def clean_name(self):
        return re.sub(r'\s+', ' ', self.cleaned_data['name'].lower().strip())

    def clean_slug(self):
        return slugify(self.cleaned_data['name'])

    def clean_rules_text(self):
        rules_text = self.cleaned_data['rules_text']
        rules_text = [re.sub(r'\s+', ' ', line.strip())
            for line in rules_text.split('\n')]
        rules_text = '\n'.join(line for line in rules_text if line)
        return rules_text

    def clean_other_card(self):
        other_card = self.cleaned_data['other_card']
        if other_card == self.instance:
            raise forms.ValidationError(
                'A card\'s other card cannot be itself.')
        return other_card

    def clean(self):
        cleaned_data = self.cleaned_data
        kind = cleaned_data.get('kind')
        other_card = cleaned_data.get('other_card')
        if kind == magic.models.Card.KIND_CHOICES[0][0]:
            if other_card is not None:
                raise forms.ValidationError(
                    'A normal card cannot have an other card.')
        elif other_card is None:
            raise forms.ValidationError(
                'A non-normal card must have its other card specified.')
        return cleaned_data
