from django import forms
import re


class GathererTextForm(forms.Form):
    # pylint: disable=R0904
    name = forms.CharField()
    cost = forms.CharField(required=False)
    color = forms.CharField(required=False)
    type = forms.CharField()
    pow_tgh = forms.CharField(required=False)
    hand_life = forms.CharField(required=False)
    loyalty = forms.CharField(required=False)
    rules_text = forms.CharField(required=False)
    set_rarity = forms.CharField()

    @staticmethod
    def clean_string(string, lower=True):
        string = re.sub(r'\s+', ' ', string)
        string = string.strip()
        if lower:
            string = string.lower()
        return string

    def clean_name(self):
        data = self.cleaned_data['name']
        data = self.clean_string(data)
        match = re.search(r'\((.*)\)', data)
        if match:
            data = match.group(1)
        return data

    def clean_cost(self):
        data = self.cleaned_data['cost']
        data = self.clean_string(data)
        data = re.findall('(\d+|[a-z])|\((\d+|[a-z])/(\d+|[a-z])\)', data)
        data = ['/'.join(symbols[0] or symbols[1:]) for symbols in data]
        return data or None

    def clean_color(self):
        return self.clean_string(self.cleaned_data['color']) or None

    def clean_type(self):
        return self.clean_string(self.cleaned_data['type'])

    def clean_pow_tgh(self):
        data = self.cleaned_data['pow_tgh']
        data = self.clean_string(data)
        data = [token for token in data[1:-1].split('/') if token]
        return data or None

    def clean_hand_life(self):
        data = self.cleaned_data['hand_life']
        data = self.clean_string(data)
        data = re.findall(r'([+-]?\d+)', data)
        return data or None

    def clean_loyalty(self):
        data = self.cleaned_data['loyalty']
        data = self.clean_string(data)
        data = data[1:-1]
        return data or None

    def clean_rules_text(self):
        data = self.cleaned_data['rules_text']
        data = [self.clean_string(line, False) for line in data.split('\n')]
        data = [line for line in data if line]
        return data or None

    def clean_set_rarity(self):
        data = self.cleaned_data['set_rarity']
        data = self.clean_string(data)
        data = data.split(', ')
        return data
