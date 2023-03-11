from rest_framework import serializers

from events.models import (
    Event,
    EventAttendee
)


class EventAttendeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventAttendee
        fields = ('event', 'user', 'created_on', 'modified_on')
        extra_kwargs = {
            'event': {'required': True},
            'user': {'required': False}
        }


class EventSerializer(serializers.ModelSerializer):
    attendees = EventAttendeeSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = ('name', 'description', 'start_date', 'end_date', 'attendees', 'capacity', 'created_by', 'created_on', 'modified_on')
        extra_kwargs = {
            'name': {'required': True},
            'description': {'required': True},
            'start_date': {'required': True},
            'end_date': {'required': True}
        }
