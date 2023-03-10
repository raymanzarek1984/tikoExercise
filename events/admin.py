from django.contrib import admin

from events.models import (
    Event
)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'start_date', 'end_date', 'created_by', 'created_on', 'modified_on']
    search_fields = ['name', 'description', 'start_date', 'end_date', 'created_by__username']
    readonly_fields = ['created_by', 'created_on', 'modified_on']
