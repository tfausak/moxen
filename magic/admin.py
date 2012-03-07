from django.contrib import admin
import magic.models


class SuperTypeAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']
admin.site.register(magic.models.SuperType, SuperTypeAdmin)
