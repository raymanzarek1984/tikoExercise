from django.urls import path

from events.apps import EventsConfig
from events import views

app_name = EventsConfig.name

urlpatterns = [
    path('', views.EventListCreateView.as_view(), name='list'),
    path('instance/<int:pk>/', views.EventGetView.as_view(), name='get'),
    path('instance/<int:pk>/update/', views.EventUpdateDeleteView.as_view(), name='update'),
    path('instance/<int:pk>/delete/', views.EventUpdateDeleteView.as_view(), name='delete'),
    path('attendee/', views.EventAttendeeRegisterView.as_view(), name='register-attendee'),
    path('attendee/<int:pk>/', views.EventAttendeeUnregisterView.as_view(), name='unregister-attendee'),
]
