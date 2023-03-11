from django.contrib import admin

from events.models import (
    Event,
    EventAttendee
)


class EventAttendeeInlineAdminForm(admin.TabularInline):
    fields = ['event', 'user']
    model = EventAttendee
    extra = 1


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    inlines = [EventAttendeeInlineAdminForm]
    fields = ['name', 'description', 'start_date', 'end_date', 'capacity', 'created_by']
    list_display = ['name', 'description', 'start_date', 'end_date', 'capacity', 'show_attendees', 'created_by', 'created_on', 'modified_on']
    search_fields = ['name', 'description', 'start_date', 'end_date', 'created_by__username']
    readonly_fields = ['created_on', 'modified_on']

    def get_changeform_initial_data(self, request):
        initial = super(EventAdmin, self).get_changeform_initial_data(request)
        initial['created_by'] = request.user
        return initial

    def show_attendees(self, instance):
        return instance.attendees.count()

    show_attendees.short_description = 'Attendees'
