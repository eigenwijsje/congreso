from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

from forms import RegistrationForm, RegistrationWizard, WorkshopsForm

urlpatterns = patterns('',
    url(r'^register/$',
        RegistrationWizard([RegistrationForm, WorkshopsForm]),
        name='register-register'),
    url(r'^register/complete/$',
        direct_to_template,
        {'template': 'register/wizard_complete.html'},
        name='register-registration-complete'),
)
