from django.db import models


class AbstractDateCreated(models.Model):
    created_on = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Created on'
    )

    class Meta:
        abstract = True


class AbstractDateModified(models.Model):
    modified_on = models.DateTimeField(
        auto_now=True,
        verbose_name='Modified on'
    )

    class Meta:
        abstract = True


class Event(AbstractDateModified, AbstractDateCreated, models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name='name'
    )
    description = models.TextField(
        default='',
        verbose_name='description'
    )
    start_date = models.DateField(
        verbose_name='start date'
    )
    end_date = models.DateField(
        verbose_name='end date'
    )
    created_by = models.ForeignKey(
        'auth.User',
        blank=True,
        null=True,
        related_name='event_creators',
        on_delete=models.CASCADE
    )

    class Meta:
        ordering = ('-start_date',)
        verbose_name = 'event'
        verbose_name_plural = 'events'

    def __str__(self):
        return self.name


class EventAttendee(AbstractDateModified, AbstractDateCreated, models.Model):
    event = models.ForeignKey(
        'events.Event',
        related_name='attendees',
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        'auth.User',
        related_name='events',
        on_delete=models.CASCADE
    )

    class Meta:
        ordering = ('event',)
        verbose_name = 'event attendee'
        verbose_name_plural = 'event attendees'

    def __str__(self):
        return f'{self.event}, Attendee {self.user_id}'
