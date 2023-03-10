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


class EventListCreateView(generics.CreateAPIView, generics.ListAPIView):
    queryset = Event.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = EventSerializer

    def get_queryset(self):
        queryset = super(EventListCreateView, self).get_queryset()
        # Handle the mine query parameter in order to filter User's own Events only
        mine = self.request.query_params.get('mine')
        if mine is not None:
            queryset = queryset.filter(created_by=self.request.user)
        return queryset

    def perform_create(self, serializer):
        # Set the created by to the request User
        serializer.validated_data['created_by'] = self.request.user
        serializer.save()


class EventGetView(generics.RetrieveAPIView):
    queryset = Event.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = EventSerializer


class EventUpdateDeleteView(generics.DestroyAPIView, generics.UpdateAPIView):
    queryset = Event.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = EventSerializer

    def get_object(self):
        obj = super(EventUpdateDeleteView, self).get_object()
        if obj.created_by != self.request.user:
            raise exceptions.PermissionDenied({'created_by': 'It is not allowed to edit or delete other users\' events.'})
        return obj


class EventAttendeeRegisterView(generics.CreateAPIView):
    queryset = EventAttendee.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = EventAttendeeSerializer

    def perform_create(self, serializer):
        if serializer.validated_data['event'].start_date < timezone.now().date():
            raise exceptions.PermissionDenied({'event': 'It is not allowed to register or unregister to past events.'})
        # Set the user to request User
        serializer.validated_data['user'] = self.request.user
        super(EventAttendeeRegisterView, self).perform_create(serializer)


class EventAttendeeUnregisterView(generics.DestroyAPIView):
    queryset = EventAttendee.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = EventAttendeeSerializer

    def get_object(self):
        obj = super(EventAttendeeUnregisterView, self).get_object()
        if obj.event.start_date < timezone.now().date():
            raise exceptions.PermissionDenied({'event': 'It is not allowed to register or unregister to past events.'})
        if obj.user != self.request.user:
            raise exceptions.PermissionDenied({'user': 'It is not allowed to register or unregister other users.'})
        return obj
