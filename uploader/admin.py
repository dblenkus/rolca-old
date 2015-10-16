from __future__ import absolute_import, division, print_function, unicode_literals

from django.contrib import admin

from .models import Salon, Theme, File, Photo


class ThemeInline(admin.TabularInline):
    model = Theme
    extra = 1


class JudgeInline(admin.TabularInline):
    model = Salon.judges.through  # pylint: disable=no-member


class SalonAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ('title',)}),
        ('Dates', {'fields': (('start_date', 'end_date'),
                              ('jury_date', 'results_date'))}),
    ]

    inlines = [ThemeInline, JudgeInline]

    list_display = ('title', 'start_date', 'end_date', 'is_active')
    list_filter = ['start_date', 'end_date', 'results_date']
    search_fields = ['title']


# admin.site.unregister(Groups)

admin.site.register(Salon, SalonAdmin)
admin.site.register(Photo)
admin.site.register(File)
