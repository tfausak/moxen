from django.contrib import admin
import magic.models


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


class CardAtomAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']
admin.site.register(magic.models.CardAtom, CardAtomAdmin)


class BlockAdmin(admin.ModelAdmin):
    filter_horizontal = ['sets']
    search_fields = ['name']
admin.site.register(magic.models.Block, BlockAdmin)


class FormatAdmin(admin.ModelAdmin):
    filter_horizontal = ['sets']
    search_fields = ['name']
admin.site.register(magic.models.Format, FormatAdmin)


class LegalityAdmin(admin.ModelAdmin):
    list_display = ['card', 'format', 'status']
    list_filter = ['format', 'status']
    search_fields = ['card__card_atom__name']
admin.site.register(magic.models.Legality, LegalityAdmin)
