from __future__ import absolute_import, division, print_function, unicode_literals

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import UserProfileChangeForm, UserProfileCreationForm
from .models import UserProfile


class UserProfileAdmin(UserAdmin):
    form = UserProfileChangeForm
    add_form = UserProfileCreationForm

    fieldsets = (
        (None, {'fields': ('first_name', 'last_name', 'email', 'password')}),
        ('School', {'fields': ('school', 'mentor')}),
        ('Dates', {'fields': ('date_joined', 'last_login'),
                   'classes': ('collapse',)}),
        ('Administration', {'fields': ('is_active', 'is_superuser', 'is_staff'),
                            'classes': ('collapse',)}),
    )

    add_fieldsets = (
        (None, {'fields': ('email', 'first_name', 'last_name', 'password1', 'password2'),
                'classes': ('wide',)}),
    )

    readonly_fields = ['id', 'date_joined', 'last_login']

    list_display = ['__str__', 'email']
    list_filter = []

    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email', 'first_name', 'last_name')


admin.site.register(UserProfile, UserProfileAdmin)
