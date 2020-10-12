from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


class CustomUserAdmin(UserAdmin):
    list_display = ('first_name', 'last_name', 'email',)
    list_filter = ('first_name', 'email',)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
