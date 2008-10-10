from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _

from datetime import datetime

class Category(models.Model):
    name = models.CharField(_('name'), max_length=16)
    slug = models.SlugField(_('slug'), max_length=16)

    class Meta:
        ordering = ('name',)
        verbose_name = _('category')
        verbose_name_plural = _('categories')

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('category-detail', [self.slug])

class Entry(models.Model):
    author = models.ForeignKey(User, related_name='entries', 
        verbose_name=_('author'))
    categories = models.ManyToManyField(Category, related_name='entries',
        verbose_name=_('categories'))
    title = models.CharField(_('title'), max_length=64)
    slug = models.SlugField(_('slug'), max_length=64)
    body = models.TextField(_('body'))
    posted = models.DateTimeField(default=datetime.now)
    last_updated = models.DateTimeField(blank=True, null=True)

    class Meta:
        get_latest_by = 'posted'
        ordering = ('-posted',)
        verbose_name = _('entry')
        verbose_name_plural = _('entries')

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('entry-detail', (),
            {'year': self.posted.strftime('%Y'),
                'month': self.posted.strftime('%m'),
                'day': self.posted.strftime('%d'),
                'slug': self.slug})
    
    def save(self):
        if self.pk:
            self.last_updated = datetime.now()

        super(Entry, self).save()
