from django.contrib import admin
import magic.models


class CardAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']
admin.site.register(magic.models.Card, CardAdmin)
