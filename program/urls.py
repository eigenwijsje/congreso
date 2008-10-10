from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

from views import submit_proposal

urlpatterns = patterns('',
    url(r'^submit/$',
        submit_proposal,
        name='program-submit-proposal'),
    url(r'^submit/complete/',
        direct_to_template,
        {'template': 'program/submit_proposal_complete.html'},
        name='program-submit-proposal-complete'),
)
