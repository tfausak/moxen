# pylint: disable=R0904
from django.contrib import admin
import app.moxen.models


class UserProfileAdmin(admin.ModelAdmin):
    search_fields = ['user__username']
admin.site.register(app.moxen.models.UserProfile, UserProfileAdmin)
