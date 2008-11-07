from django import forms

from models import Registration

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Registration
        exclude = ('event', 'amount_paid', 'notes', 'paid', 'registered')
