from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render_to_response

from models import Entry

def author_entry_list(request, username):
    author = get_object_or_404(User, username=username)
    entry_list = Entry.objects.filter(author=author)

    return render_to_response('blog/author_entry_list.html',
        {'entry_list': entry_list,
            'author': author})
