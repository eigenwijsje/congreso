from django import forms

from models import Author, Proposal

class AuthorForm(forms.ModelForm):
    short_bio = forms.CharField(widget=forms.Textarea())

    class Meta:
        model = Author

class ProposalForm(forms.ModelForm):
    summary = forms.CharField(widget=forms.Textarea())

    class Meta:
        exclude = ('author', 'status', 'submitted', 'approved', 'rejected')
        model = Proposal
