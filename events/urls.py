from django.urls import path

from events.apps import EventsConfig
from events import views

app_name = EventsConfig.name

urlpatterns = [
    path('', views.EventListView.as_view(), name='list'),
    path('create/', views.EventCreateView.as_view(), name='create'),
    path('<int:pk>/', views.EventGetView.as_view(), name='get'),
    path('update/<int:pk>/', views.EventUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', views.EventDeleteView.as_view(), name='delete'),
    path('register-attendee/', views.EventAttendeeRegisterView.as_view(), name='register-attendee'),
    path('unregister-attendee/<int:pk>/', views.EventAttendeeUnregisterView.as_view(), name='unregister-attendee'),
]
