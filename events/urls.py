from django.urls import path

from events.apps import EventsConfig
from events.views import (
    EventListCreateView,
    EventGetUpdateDeleteView
)

app_name = EventsConfig.name

urlpatterns = [
    path('', EventListCreateView.as_view(), name='list'),
    path('instance/<int:pk>/', EventGetUpdateDeleteView.as_view(), name='instance'),
]
