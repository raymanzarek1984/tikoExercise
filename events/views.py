from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from events.models import (
    Event
)
from events.serializers import (
    EventSerializer
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
        # Set the created by request User
        serializer.validated_data['created_by'] = self.request.user
        serializer.save()


class EventGetUpdateDeleteView(generics.DestroyAPIView, generics.UpdateAPIView, generics.RetrieveAPIView):
    queryset = Event.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = EventSerializer

    def get_queryset(self):
        queryset = super(EventGetUpdateDeleteView, self).get_queryset() \
            .filter(created_by=self.request.user)
        return queryset
