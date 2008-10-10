from django.contrib import admin

from models import Event, Registration, Workshop, WorkshopRegistration

class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'starts', 'ends', 'registration_closes',
            'registration_is_closed', 'registrations_count')
    list_filter = ('registration_is_closed',)
    search_fields = ('name', 'description')

class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'amount_due', 'amount_paid',
        'status')
    search_fields = ('first_name', 'last_name', 'notes')

class WorkshopAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'duration', 'cost', 'registrations_count')
    list_filter = ('event',)
    prepopulated_fields = {'slug': ('name',)}

class WorkshopRegistrationAdmin(admin.ModelAdmin):
    list_display = ('registration', 'workshop', 'registered')

admin.site.register(Event, EventAdmin)
admin.site.register(Registration, RegistrationAdmin)
admin.site.register(Workshop, WorkshopAdmin)
admin.site.register(WorkshopRegistration, WorkshopRegistrationAdmin)
