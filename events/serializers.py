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
            'start_date': {'required': True},
            'end_date': {'required': True}
        }

    def create(self, validated_data):
        obj = self.Meta.model.objects.create(
            name=validated_data['name'],
            description=validated_data['description'],
            start_date=validated_data['start_date'],
            end_date=validated_data['end_date'],
            created_by=validated_data['created_by']
        )
        return obj
