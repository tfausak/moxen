# pylint: disable=R0904
from django.contrib import admin
import users.models


class UserProfileAdmin(admin.ModelAdmin):
    search_fields = ['user__username']
admin.site.register(users.models.UserProfile, UserProfileAdmin)
