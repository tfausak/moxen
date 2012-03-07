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
