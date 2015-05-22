from django.contrib import admin

from .models import Application, Workshop


class WorkshopAdmin(admin.ModelAdmin):
    list_display = ['__unicode__', 'count', 'start_date', 'end_date',
                    'location', 'instructor']


class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'institution_name', 'workshop',
                    'n_of_applicants', 'institution']


admin.site.register(Application, ApplicationAdmin)
admin.site.register(Workshop, WorkshopAdmin)
