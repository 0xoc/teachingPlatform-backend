from django.contrib import admin
from .models import *


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'first_name', 'last_name']

    @staticmethod
    def username(up):
        return up.user.username

    @staticmethod
    def first_name(up):
        return up.user.first_name

    @staticmethod
    def last_name(up):
        return up.user.last_name


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(ClassRoom)
