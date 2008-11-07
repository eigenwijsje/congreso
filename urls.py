from django.conf.urls.defaults import *
from django.contrib import admin

from congreso.views import homepage

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
    (r'^workshops/', include('congreso.workshops.urls')),
)
