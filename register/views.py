from django.conf import settings
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template.loader import render_to_string

from forms import RegistrationForm

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            registration = form.save(commit=False)
            registration.save()

            current_site = Site.objects.get_current()

            subject = render_to_string('register/confirmation_email_subject.txt',
                {'site': current_site})
            subject = ''.join(subject.splitlines())
            message = render_to_string('register/confirmation_email.txt',
                {'registration': registration})
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL,
                [registration.email])

            return HttpResponseRedirect(reverse('register-registration-complete'))
    else:
        form = RegistrationForm()

    return render_to_response('register/registration_form.html', {'form': form})
