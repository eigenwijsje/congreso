from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response

from forms import AuthorForm, ProposalForm

def submit_proposal(request):
    if request.method=='POST':
        author_form = AuthorForm(request.POST)
        proposal_form = ProposalForm(request.POST, request.FILES)
        
        if author_form.is_valid() and proposal_form.is_valid:
            author = author_form.save(commit=False)
            author.save()
            
            proposal = proposal_form.save(commit=False)
            proposal.author = author
            proposal.save()

            return HttpResponseRedirect(reverse('program-submit-proposal-complete'))
    else:
        author_form = AuthorForm()
        proposal_form = ProposalForm()

    return render_to_response('program/submit_proposal_form.html',
        {'author_form': author_form, 'proposal_form': proposal_form})
