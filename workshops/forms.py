from django import forms

from congreso.register.models import Event

from models import Registration, Workshop

class RegistrationForm(forms.ModelForm):
    event = Event.objects.get(is_current=True)
    queryset = Workshop.objects.filter(event=event)

    values = [w for w in queryset if w.is_open_for_registration]
 
    choices = [(w.id, u'%s, %s' % (w.title, w.trainer)) for w in values]
 
    workshops = forms.MultipleChoiceField(choices=choices,
        widget=forms.CheckboxSelectMultiple())

    class Meta:
        exclude = ('amount_paid', 'notes', 'registered', 'paid')
        model = Registration
