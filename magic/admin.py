from django.contrib import admin
import magic.forms
import magic.models


class CardAdmin(admin.ModelAdmin):
    form = magic.forms.CardForm
admin.site.register(magic.models.Card, CardAdmin)
