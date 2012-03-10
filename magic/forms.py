from django import forms
import magic.constants
import magic.models
import re


class CardForm(forms.ModelForm):
    class Meta:
        model = magic.models.Card

    def clean_name(self):
        data = self.cleaned_data['name']
        data = re.sub(r'\s+', ' ', data.lower().strip())
        match = re.search(r'\(([^(]*)\)$', data)
        if match:
            data = match.group(1)
        return data

    def clean_slug(self):
        data = self.cleaned_data['name']
        data = data.translate(magic.constants.TRANSLATION)
        data = re.sub('[^-0-9a-z _]', '', data)
        data = re.sub(' ', '-', data)
        data = re.sub('-+', '-', data)
        data = re.sub('^-|-$', '', data)
        return data
