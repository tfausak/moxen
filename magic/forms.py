from django import forms
import magic.models


class CardForm(forms.ModelForm):
    class Meta:
        model = magic.models.Card
