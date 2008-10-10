from django.shortcuts import render_to_response

from blog.models import Entry
from contact_form.forms import ContactForm

def homepage(request):
    entry = Entry.objects.latest()
    form = ContactForm(request=request)
    return render_to_response('homepage.html', {'entry': entry, 'form': form})
