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


class CardAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']
admin.site.register(magic.models.Card, CardAdmin)
