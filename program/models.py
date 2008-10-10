from django.contrib.auth.models import User, get_hexdigest
from django.db import models
from django.utils.translation import ugettext_lazy as _

from datetime import datetime

class Author(models.Model):
    first_name = models.CharField(_('first name'), max_length=32)
    last_name = models.CharField(_('last name'), max_length=32)
    email = models.EmailField(_('e-mail address'))
    short_bio = models.TextField(_('short bio'))

    class Meta:
        ordering = ('last_name', 'first_name')
        verbose_name = _('author')
        verbose_name_plural = _('authors')

    def __unicode__(self):
        return '%s, %s' % (self.last_name, self.first_name)

    @models.permalink
    def get_absolute_url(self):
        return ('author-detail', [str(self.id)])

class Proposal(models.Model):
    STATUS_CHOICES = (
        (1, _('submitted')),
        (2, _('rejected')),
        (4, _('accepted'))
    )
    author = models.ForeignKey(Author, related_name='proposals',
        verbose_name=_('author'))
    title = models.CharField(_('title'), max_length=128)
    summary = models.TextField(_('summary'))
    attachment = models.FileField(_('attachment file'), 
        upload_to='attachments/%Y/%m/%d')
    status = models.IntegerField(_('status'), choices=STATUS_CHOICES, default=1)
    submitted = models.DateTimeField(default=datetime.now, editable=False)
    approved = models.DateTimeField(_('date approved'), blank=True, 
        editable=False, null=True)
    rejected = models.DateTimeField(_('date rejected'), blank=True, 
        editable=False, null=True)

    class Meta:
        ordering = ('title',)
        verbose_name = _('proposal')
        verbose_name_plural = _('proposals')

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('proposal-detail', [str(self.id)])

    def save(self):
        if self.status==4:
            self.approved = datetime.now()
        
        if self.status==2:
            self.rejected = datetime.now()

        super(Proposal, self).save()

    def total_rating(self):
        return sum([r.rating for r in self.reviews.all()])
    total_rating.short_description = _('total rating')

    def reviews_count(self):
        return self.reviews.count()
    reviews_count.short_description = _('review count')

    def average_rating(self):
        if self.reviews.count()>0:
            return self.total_rating()/self.reviews.count()
        else:
            return None
    average_rating.short_description = _('average rating')

class Review(models.Model):
    RATING_CHOICES = tuple([(n, str(n)) for n in range(1,6)])

    proposal = models.ForeignKey(Proposal, related_name='reviews',
        verbose_name=_('proposal'))
    reviewer = models.ForeignKey(User, related_name='reviews',
        verbose_name=_('reviewer'))
    rating = models.IntegerField(_('rating'), choices=RATING_CHOICES)
    comment = models.TextField(_('comment'))
    reviewed = models.DateTimeField(default=datetime.now, editable=False)

    class Meta:
        ordering = ('-reviewed',)
        unique_together = ('proposal', 'reviewer')
        verbose_name = _('review')
        verbose_name_plural = _('reviews')

    def __unicode__(self):
        return _('%(reviewer)s rated %(rating)i on %(proposal)s') % \
            {'reviewer': self.reviewer.username,
                'rating': self.rating,
                'proposal': self.proposal.title}
