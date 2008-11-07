from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

from views import register

urlpatterns = patterns('',
    url(r'^register/$',
        register,
        name='register-register'),
    url(r'^register/complete/$',
        direct_to_template,
        {'template': 'register/registration_complete.html'},
        name='register-registration-complete'),
)
