# -*- coding: utf-8 -*-
from django.contrib import admin
from .forms import AdminUserChangeForm, AdminUserAddForm
from .models import *
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

class CustomUserAdmin(UserAdmin):
    form = AdminUserChangeForm
    add_form = AdminUserAddForm
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': (
            'first_name',
            'patronymic',
            'last_name',
            'telephone',
            'email',
            'birthday',
            'group',
            'office',
            'timetable',
            'p_num',
            'fired',
            )}),
        (_('Permissions'), {'fields': (
            'is_active',
            'is_staff',
            'is_superuser',
            'groups',
            'user_permissions')}),
        (_('Important dates'), {'fields': (
            'last_login',
            'date_joined')}),
        )
    add_fieldsets = ((None, {'classes': ('wide',),
        'fields': (
            'username',
            'password1',
            'password2',
            # 'p_num',
            )}),)

admin.site.unregister(User)
# admin.site.register(User, UserAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(s_group)
admin.site.register(s_office)
admin.site.register(s_timetable)
admin.site.register(s_system)
admin.site.register(s_fault)
admin.site.register(s_drop_lift)
admin.site.register(s_lift)
admin.site.register(s_fault_lift)
admin.site.register(s_objects)
admin.site.register(s_commit)
