from django.contrib import admin
import magic.forms
import magic.models


class ColorAdmin(admin.ModelAdmin):
    form = magic.forms.ColorForm
    search_fields = ['name']
admin.site.register(magic.models.Color, ColorAdmin)


class ManaSymbolAdmin(admin.ModelAdmin):
    form = magic.forms.ManaSymbolForm
    list_filter = ['value', 'colors']
    search_fields = ['name']
admin.site.register(magic.models.ManaSymbol, ManaSymbolAdmin)


class ManaCostAdmin(admin.ModelAdmin):
    form = magic.forms.ManaCostForm
    list_filter = ['mana_symbol']
    search_fields = ['mana_symbol__name']
admin.site.register(magic.models.ManaCost, ManaCostAdmin)


class SuperTypeAdmin(admin.ModelAdmin):
    form = magic.forms.SuperTypeForm
    prepopulated_fields = {'slug': ['name']}
    search_fields = ['name']
admin.site.register(magic.models.SuperType, SuperTypeAdmin)


class CardTypeAdmin(admin.ModelAdmin):
    form = magic.forms.CardTypeForm
    prepopulated_fields = {'slug': ['name']}
    search_fields = ['name']
admin.site.register(magic.models.CardType, CardTypeAdmin)


class SubTypeAdmin(admin.ModelAdmin):
    form = magic.forms.SubTypeForm
    prepopulated_fields = {'slug': ['name']}
    search_fields = ['name']
admin.site.register(magic.models.SubType, SubTypeAdmin)


class SetAdmin(admin.ModelAdmin):
    form = magic.forms.SetForm
    list_display = ['name', 'slug', 'release_date']
    search_fields = ['name']
admin.site.register(magic.models.Set, SetAdmin)


class RarityAdmin(admin.ModelAdmin):
    form = magic.forms.RarityForm
    search_fields = ['name']
admin.site.register(magic.models.Rarity, RarityAdmin)


class RulingAdmin(admin.ModelAdmin):
    list_display = ['text', 'date']
    list_filter = ['date']
    search_fields = ['text']
admin.site.register(magic.models.Ruling, RulingAdmin)


class CardAdmin(admin.ModelAdmin):
    form = magic.forms.CardForm
    list_filter = ['reserved', 'kind', 'super_types', 'card_types']
    prepopulated_fields = {'slug': ['name']}
    search_fields = ['name']
admin.site.register(magic.models.Card, CardAdmin)


class PrintingAdmin(admin.ModelAdmin):
    list_display = ['card', 'set', 'rarity', 'number']
    list_filter = ['rarity', 'set']
    search_fields = ['card__name']
admin.site.register(magic.models.Printing, PrintingAdmin)


class BlockAdmin(admin.ModelAdmin):
    filter_horizontal = ['sets']
    prepopulated_fields = {'slug': ['name']}
    search_fields = ['name']
admin.site.register(magic.models.Block, BlockAdmin)


class FormatAdmin(admin.ModelAdmin):
    filter_horizontal = ['sets']
    prepopulated_fields = {'slug': ['name']}
    search_fields = ['name']
admin.site.register(magic.models.Format, FormatAdmin)


class LegalityAdmin(admin.ModelAdmin):
    list_display = ['card', 'format', 'status']
    list_filter = ['status', 'format']
    search_fields = ['card__name']
admin.site.register(magic.models.Legality, LegalityAdmin)


class DeckAdmin(admin.ModelAdmin):
    list_display = ['name', 'user']
    search_fields = ['name']
admin.site.register(magic.models.Deck, DeckAdmin)


class DeckCardAdmin(admin.ModelAdmin):
    list_filter = ['number']
    search_fields = ['card__name']
admin.site.register(magic.models.DeckCard, DeckCardAdmin)


class CollectionAdmin(admin.ModelAdmin):
    search_fields = ['user__username']
admin.site.register(magic.models.Collection, CollectionAdmin)


class CollectionCardAdmin(admin.ModelAdmin):
    search_fields = ['card__name']
admin.site.register(magic.models.CollectionCard, CollectionCardAdmin)


class CollectionPrintingAdmin(admin.ModelAdmin):
    search_fields = ['printing__card__name']
admin.site.register(magic.models.CollectionPrinting, CollectionPrintingAdmin)
