from django.conf.urls.defaults import *
from django.views.generic.date_based import archive_index
from django.views.generic.date_based import object_detail as entry_detail
from django.views.generic.list_detail import object_detail, object_list

from models import Category, Entry
from views import author_entry_list

category_info = {
    'queryset': Category.objects.all(),
    'template_object_name': 'category'
}

entry_info = {
    'queryset': Entry.objects.all(),
}

urlpatterns = patterns('',
    url(r'^category/(?P<slug>[\w-]+)/$',
        object_detail, 
        category_info,
        name='category-detail'),
    url(r'^author/(?P<username>\w+)/$',
        author_entry_list, 
        name='author-entry-list'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[\w-]+)/$',
        entry_detail,
        dict(entry_info, date_field='posted', month_format='%m', slug_field='slug', template_object_name='entry'),
        name='entry-detail'),
    url(r'^$',
        archive_index,
        dict(entry_info, date_field='posted'),
        name='blog-entry-archive-index'),
    )
