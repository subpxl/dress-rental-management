from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group


class UserAdminBase(UserAdmin):
    model = User
    list_display = ('email', 'first_name', 'last_name',
                    'username', 'role', 'is_active')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    readonly_fields=('password',)

admin.site.unregister(Group)
# Register your models here.
admin.site.register(User, UserAdminBase)
admin.site.register(Address)