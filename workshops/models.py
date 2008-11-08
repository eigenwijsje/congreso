from django.db import models
from django.utils.translation import ugettext_lazy as _

from datetime import datetime, time

from congreso.register.models import Event

class Workshop(models.Model):
    event = models.ForeignKey(Event, related_name='workshops',
        verbose_name=_('event'))
    title = models.CharField(_('title'), max_length=128)
    slug = models.SlugField(_('slug'), max_length=32)
    trainer = models.CharField(_('trainer'), max_length=64)
    description = models.TextField(_('description'))
    duration = models.TimeField(_('duration'), default=time(2))
    cost = models.IntegerField(_('cost'), default=0)
    max_registrations = models.IntegerField(_('maximal registrations'))
    
    class Meta:
        ordering = ('title',)
        unique_together = ('event', 'title')
        verbose_name = _('workshop')
        verbose_name_plural = _('workshops')

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('workshop-detail', [self.slug])

    def registration_count(self):
        return self.registrations.count()
    registration_count.short_description = _('registration count')

    def is_open_for_registration(self):
        return self.registrations.count() < self.max_registrations
    is_open_for_registration.short_description = _('is open for registration')

class Registration(models.Model):
    first_name = models.CharField(_('first name'), max_length=32)
    last_name = models.CharField(_('last name'), max_length=32)
    id_number = models.CharField(_('identification number'), max_length=16)
    receipt_number = models.CharField(_('receipt number'), max_length=32)
    email = models.EmailField(_('e-mail address'))
    amount_paid = models.IntegerField(_('amount paid'), default=0)
    notes = models.TextField(_('notes'), blank=True)
    workshops = models.ManyToManyField(Workshop, 
        related_name='registrations', verbose_name=_('workshops'))
    registered = models.DateTimeField(default=datetime.now, editable=False)
    paid = models.DateTimeField(_('date paid'), blank=True, null=True)    
    
    class Meta:
        ordering = ('last_name', 'first_name')
        verbose_name = _('registration')
        verbose_name_plural = _('registrations')

    def __unicode__(self):
        return '%s, %s' % (self.last_name, self.first_name)

    def save(self):
        if self.amount_paid>0 and not self.paid:
            self.paid = datetime.now()

        super(Registration, self).save()

    def amount_due(self):
        return sum([w.cost for w in self.workshops.all()])
    amount_due.short_description = _('amount due')
