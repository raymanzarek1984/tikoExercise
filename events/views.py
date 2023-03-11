from django.utils import timezone
from rest_framework import generics
from rest_framework import exceptions
from rest_framework.permissions import IsAuthenticated

from events.models import (
    Event,
    EventAttendee
)
from events.serializers import (
    EventSerializer,
    EventAttendeeSerializer,
)


class EventListView(generics.ListAPIView):
    """
    Retrieves a list of event entries, related to :model:`events.Event`.
    """
    queryset = Event.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = EventSerializer

    def get_queryset(self):
        queryset = super(EventListView, self).get_queryset()
        # Handle the mine query parameter in order to filter User's own Events only
        mine = self.request.query_params.get('mine')
        if mine is not None:
            queryset = queryset.filter(created_by=self.request.user)
        return queryset


class EventCreateView(generics.CreateAPIView):
    """
    Creates an event entry, related to :model:`events.Event`.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = EventSerializer

    def perform_create(self, serializer):
        # Set the created by to the request User
        serializer.validated_data['created_by'] = self.request.user
        serializer.save()


class EventGetView(generics.RetrieveAPIView):
    """
    Retrieves an event entry, related to :model:`events.Event`.
    """
    queryset = Event.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = EventSerializer


class EventUpdateView(generics.UpdateAPIView):
    """
    Updates an event entry, related to :model:`events.Event`.
    """
    queryset = Event.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = EventSerializer

    def get_object(self):
        obj = super(EventUpdateView, self).get_object()
        if obj.created_by != self.request.user:
            raise exceptions.PermissionDenied({'created_by': 'It is not allowed to edit other users\' events.'})
        return obj


class EventDeleteView(generics.DestroyAPIView):
    """
    Deletes an event entry, related to :model:`events.Event`.
    """
    queryset = Event.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = EventSerializer

    def get_object(self):
        obj = super(EventDeleteView, self).get_object()
        if obj.created_by != self.request.user:
            raise exceptions.PermissionDenied({'created_by': 'It is not allowed to delete other users\' events.'})
        return obj


class EventAttendeeRegisterView(generics.CreateAPIView):
    """
    Registers an attendee to an event entry, related to :model:`events.EventAttendee`.
    Attendees cannot register to past events.
    Attendees can be registered until capacity is reached.
    Attendees can only register once.
    """
    queryset = EventAttendee.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = EventAttendeeSerializer

    def perform_create(self, serializer):
        event = serializer.validated_data['event']
        if event.start_date < timezone.now().date():
            raise exceptions.PermissionDenied({'event': 'It is not allowed to register to past events.'})
        if event.capacity and event.attendees.count() >= event.capacity:
            raise exceptions.PermissionDenied({'event': 'It is not allowed to register to a full event.'})
        # Check for unique attendees
        if self.request.user.id in event.attendees.select_related('event', 'user').values_list('user_id', flat=True):
            raise exceptions.PermissionDenied({'event': 'It is not allowed to register more than once to an event.'})
        # Set the user to request User
        serializer.validated_data['user'] = self.request.user
        super(EventAttendeeRegisterView, self).perform_create(serializer)


class EventAttendeeUnregisterView(generics.DestroyAPIView):
    """
    Unregisters an attendee from an event entry, related to :model:`events.EventAttendee`.
    Attendees cannot unregister from past events.
    Attendees cannot unregister other attendees.
    """
    queryset = EventAttendee.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = EventAttendeeSerializer

    def get_object(self):
        obj = super(EventAttendeeUnregisterView, self).get_object()
        if obj.event.start_date < timezone.now().date():
            raise exceptions.PermissionDenied({'event': 'It is not allowed to unregister from past events.'})
        if obj.user != self.request.user:
            raise exceptions.PermissionDenied({'user': 'It is not allowed to unregister other attendees.'})
        return obj
