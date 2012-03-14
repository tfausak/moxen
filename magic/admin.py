# pylint: disable=R0904
from django.contrib import admin
import magic.models


class ManaSymbolAdmin(admin.ModelAdmin):
    search_fields = ['name']
admin.site.register(magic.models.ManaSymbol, ManaSymbolAdmin)


class ManaCostAdmin(admin.ModelAdmin):
    list_filter = ('mana_symbols',)
    search_fields = ['mana_symbols__name']
admin.site.register(magic.models.ManaCost, ManaCostAdmin)


class SuperTypeAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']
admin.site.register(magic.models.SuperType, SuperTypeAdmin)


class CardTypeAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']
admin.site.register(magic.models.CardType, CardTypeAdmin)


class SubTypeAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']
admin.site.register(magic.models.SubType, SubTypeAdmin)


class SetAdmin(admin.ModelAdmin):
    search_fields = ['name']
admin.site.register(magic.models.Set, SetAdmin)


class RarityAdmin(admin.ModelAdmin):
    search_fields = ['name']
admin.site.register(magic.models.Rarity, RarityAdmin)


class ColorAdmin(admin.ModelAdmin):
    search_fields = ['name']
admin.site.register(magic.models.Color, ColorAdmin)


class CardAdmin(admin.ModelAdmin):
    list_filter = ('kind', 'super_types', 'card_types')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']
admin.site.register(magic.models.Card, CardAdmin)


class PrintingAdmin(admin.ModelAdmin):
    list_display = ('card', 'set', 'rarity')
    list_filter = ('rarity', 'set')
    search_fields = ['card__name']
admin.site.register(magic.models.Printing, PrintingAdmin)


class BlockAdmin(admin.ModelAdmin):
    filter_horizontal = ['sets']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']
admin.site.register(magic.models.Block, BlockAdmin)


class FormatAdmin(admin.ModelAdmin):
    filter_horizontal = ['sets']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']
admin.site.register(magic.models.Format, FormatAdmin)


class LegalityAdmin(admin.ModelAdmin):
    list_display = ['card', 'format', 'status']
    list_filter = ['status', 'format']
    search_fields = ['card__name']
admin.site.register(magic.models.Legality, LegalityAdmin)


class UserProfileAdmin(admin.ModelAdmin):
    search_fields = ['user__username']
admin.site.register(magic.models.UserProfile, UserProfileAdmin)
