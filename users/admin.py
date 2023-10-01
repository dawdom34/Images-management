from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Account


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'date_joined', 'last_login', 'is_admin','is_staff')
    search_fields = ('username',)
    readonly_fields = ('id', 'date_joined', 'last_login')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(Account, CustomUserAdmin)