from django.contrib.sites.models import Site
from django.db import models
from django.utils.translation import ugettext_lazy as _

from datetime import datetime, time

class Event(models.Model):
    name = models.CharField(_('name'), max_length=64)
    slug = models.SlugField(_('slug'), max_length=16)
    description = models.TextField(_('description'))
    is_current = models.BooleanField(_('is current'), default=True)
    registration_is_closed = models.BooleanField(_('registration is closed'),
        default=False)
    starts = models.DateField(_('start date'))
    ends = models.DateField(_('end date'))
    registration_fee = models.IntegerField(_('registration fee'))
    registration_closes = models.DateField(_('registration close date'))

    class Meta:
        ordering = ('name',)
        verbose_name = _('event')
        verbose_name_plural = _('events')

    def __unicode__(self):
        return self.name

    def save(self):
        Event.objects.update(is_current=False)
        super(Event, self).save()

    def registrations_count(self):
        return self.registrations.count()
    registrations_count.short_description = _('registration count')

class Registration(models.Model):
    STATUS_CHOICES = (
        ('attendee', _('attendee')),
        ('helper', _('helper')),
        ('organizer', _('organizer')),
        ('speaker', _('speaker')),
        ('sponsor', _('sponsor')),
    )
    event = models.ForeignKey(Event, related_name='registrations',
        verbose_name=_('event'))
    first_name = models.CharField(_('first name'), max_length=32)
    last_name = models.CharField(_('last name'), max_length=32)
    email = models.EmailField(_('e-mail address'))
    organization = models.CharField(_('organization'), blank=True,
        max_length=64)
    phone = models.CharField(_('phone number'), max_length=16)
    address = models.CharField(_('address'), max_length=64)
    city = models.CharField(_('city'), max_length=16)
    country = models.CharField(_('country'), max_length=16)
    is_student = models.BooleanField(_('is student'), default=False)
    is_from_other_city = models.BooleanField(_('is from other city'),
         default=False)
    amount_paid = models.IntegerField(_('amount paid'), default=0)
    status = models.CharField(_('status'), choices=STATUS_CHOICES, 
        default='attendee', max_length=16)
    notes = models.TextField(_('notes'), blank=True)
    registered = models.DateTimeField(default=datetime.now, editable=False)
    paid = models.DateTimeField(_('date paid'), blank=True, null=True)    

    class Meta:
        ordering = ('last_name', 'first_name')
        verbose_name = _('registration')
        verbose_name_plural = _('registrations')

    def __unicode__(self):
        return '%s, %s' % (self.last_name, self.first_name)

    def save(self):
        if not self.pk:
            self.event = Event.objects.get(is_current=True)

        if self.amount_paid>0 and not self.paid:
            self.paid = datetime.now()

        super(Registration, self).save()

    def amount_due(self):
        if self.is_student:
            if self.is_from_other_city:
                reduction = 70
            else:
                reduction = 50
        else:
            reduction = 0

        workshops_costs = sum([w.cost for w in self.workshops.all()])

        return self.event.registration_fee + workshops_costs - reduction
    amount_due.short_description = _('amount due')

class Workshop(models.Model):
    event = models.ForeignKey(Event, related_name='workshops',
        verbose_name=_('event'))
    name = models.CharField(_('name'), max_length=32)
    title = models.CharField(_('title'), max_length=128)
    slug = models.SlugField(_('slug'), max_length=32)
    description = models.TextField(_('description'))
    duration = models.TimeField(_('duration'), default=time(2))
    cost = models.IntegerField(_('cost'), default=0)
    max_registrations = models.IntegerField(_('maximal registrations'))
    registration_is_closed = models.BooleanField(_('registration is closed'),
        default=False)
    registration_closes = models.DateField(_('registration close date'))
    starts = models.DateTimeField(_('start date'), blank=True, null=True)
    registrations = models.ManyToManyField(Registration, 
        related_name='workshops', through='WorkshopRegistration', 
        verbose_name=_('registrations'))
    added = models.DateTimeField(default=datetime.now, editable=False)
    last_updated = models.DateTimeField(_('date last updated'), blank=True,
        editable=False, null=True)
    closed = models.DateTimeField(_('date closed'), blank=True, editable=False, 
        null=True)

    class Meta:
        ordering = ('name',)
        unique_together = ('event', 'name')
        verbose_name = _('workshop')
        verbose_name_plural = _('workshops')

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('workshop-detail', [self.slug])

    def registrations_count(self):
        return self.registrations.count()
    registrations_count.short_description = _('registration count')

class WorkshopRegistration(models.Model):
    registration = models.ForeignKey(Registration,
        related_name='workshopregistrations', verbose_name=_('registration'))
    workshop = models.ForeignKey(Workshop,
        related_name='workshopregistrations', verbose_name=_('workshop'))
    registered = models.DateTimeField(editable=False, default=datetime.now)

    class Meta:
        ordering = ('-registered',)
        verbose_name = _('workshop registration')
        verbose_name_plural = _('workshop registrations')

    def __unicode__(self):
        return _('%(first_name)s %(last_name)s is registered for %(name)s') % \
            {'first_name': self.registration.first_name,
                'last_name': self.registration.last_name,
                'name': self.workshop.name}
