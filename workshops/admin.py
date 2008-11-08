from django.contrib import admin

from models import Registration, Workshop

class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'amount_due', 'amount_paid')
    search_fields = ('first_name', 'last_name', 'notes')

class WorkshopAdmin(admin.ModelAdmin):
    list_display = ('title', 'duration', 'cost', 'max_registrations',
        'registration_count')
    list_filter = ('event',)
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Registration, RegistrationAdmin)
admin.site.register(Workshop, WorkshopAdmin)
