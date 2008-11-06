from django.contrib import admin

from models import Event, Registration

class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'starts', 'ends', 'registration_closes',
            'registration_is_closed', 'registrations_count')
    list_filter = ('registration_is_closed',)
    search_fields = ('name', 'description')

class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'amount_due', 'amount_paid',
        'status')
    search_fields = ('first_name', 'last_name', 'notes')

admin.site.register(Event, EventAdmin)
admin.site.register(Registration, RegistrationAdmin)
