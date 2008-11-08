from django.conf import settings
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.loader import render_to_string

from forms import RegistrationForm
from models import Workshop

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            registration = form.save(commit=False)
            registration.save()

            for workshop in form.cleaned_data['workshops']:
                registration.workshops.add(Workshop.objects.get(id=workshop))

            current_site = Site.objects.get_current()

            subject = render_to_string('workshops/confirmation_email_subject.txt',
                {'site': current_site})
            subject = ''.join(subject.splitlines())
            message = render_to_string('workshops/confirmation_email.txt',
                {'registration': registration})
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL,
                [registration.email])
            
            return HttpResponseRedirect(reverse('workshop-registration-complete'))
    else:
        form = RegistrationForm()

    return render_to_response('workshops/registration_form.html', {'form': form})
