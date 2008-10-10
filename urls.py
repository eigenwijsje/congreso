from django.conf.urls.defaults import *
from django.contrib import admin
from django.views.generic.list_detail import object_list, object_detail

from congreso.register.models import Event, Workshop
from congreso.views import homepage

current_event = Event.objects.get(is_current=True)

workshop_info = {
        'queryset': Workshop.objects.filter(event=current_event),
        'template_object_name': 'workshop'
}

admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/(.*)', admin.site.root),
    (r'^accounts/', include('registration.urls')),
    (r'^contact/', include('contact_form.urls')),
    url(r'^$',
        homepage,
        name='homepage'),
    (r'^blog/', include('congreso.blog.urls')),
    (r'^program/', include('congreso.program.urls')),
    (r'^register/', include('congreso.register.urls')),
    url(r'^workshops/$',
        object_list,
        workshop_info,
        name='workshop-list'),
    url(r'^workshop/(?P<slug>[\w-]+)/$',
        object_detail,
        dict(workshop_info, slug_field='slug'),
        name='workshop-detail'),
)
