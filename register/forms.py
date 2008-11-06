from django.conf import settings
from django.contrib.formtools.wizard import FormWizard
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django import forms
from django.shortcuts import render_to_response
from django.template.loader import render_to_string

from models import Event, Registration, Workshop, WorkshopRegistration

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Registration
        exclude = ('event', 'amount_paid', 'notes', 'paid', 'registered')

class WorkshopsForm(forms.Form):
    event = Event.objects.get(is_current=True)

    queryset = Workshop.objects.filter(event=event,
        registration_is_closed=False)

    choices = [(w['id'], u'%s, %s Bs.' % \
        (w['title'], w['cost'])) for w in queryset.values()]

    workshops = forms.MultipleChoiceField(choices=choices, required=False,
        widget=forms.CheckboxSelectMultiple())

class RegistrationWizard(FormWizard):
    def done(self, request, form_list):
        registration_form = form_list[0]
        workshops_form = form_list[1]

        workshops_data = workshops_form.cleaned_data

        registration = registration_form.save(commit=False)
        registration.save()

        for workshop in workshops_data['workshops']:
            workshopregistration = WorkshopRegistration(registration=registration,
                workshop=Workshop.objects.get(id=int(workshop)))

            workshopregistration.save()

        current_site = Site.objects.get_current()

        subject = render_to_string('register/confirmation_email_subject.txt',
            { 'site': current_site })
        subject = ''.join(subject.splitlines())
        message = render_to_string('register/confirmation_email.txt',
            {'registration': registration})
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL,
            [registration.email])

        return HttpResponseRedirect(reverse('register-registration-complete'))

    def get_template(self, step):
        return 'register/wizard_%s.html' % step
