from django.contrib import admin
import bauble.models


class UserProfileAdmin(admin.ModelAdmin):
    search_fields = ['user__username']
admin.site.register(bauble.models.UserProfile, UserProfileAdmin)
