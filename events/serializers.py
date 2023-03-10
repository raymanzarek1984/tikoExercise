from rest_framework import serializers

from events.models import (
    Event
)


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('name', 'description', 'start_date', 'end_date', 'created_by', 'created_on', 'modified_on')
        extra_kwargs = {
            'name': {'required': True},
            'description': {'required': True},
            'start_date': {'required': True},
            'end_date': {'required': True}
        }
