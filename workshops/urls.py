from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_list, object_detail
from django.views.generic.simple import direct_to_template

from congreso.register.models import Event

from models import Workshop
from views import register

current_event = Event.objects.get(is_current=True)

workshop_info = {
    'queryset': Workshop.objects.filter(event=current_event),
    'template_object_name': 'workshop'
}

urlpatterns = patterns('',
    url(r'^$',
        object_list,
        workshop_info,
        name='workshop-list'),
    url(r'^register/$',
        register,
        name='workshop-register'),
    url(r'^(?P<slug>[\w-]+)/$',
        object_detail,
        dict(workshop_info, slug_field='slug'),
        name='workshop-detail'),
    url(r'^register/complete/$',
        direct_to_template,
        {'template': 'workshops/registration_complete.html'},
        name='workshop-registration-complete'),
)
