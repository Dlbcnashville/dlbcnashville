from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
     path('event/register', views.EventCreateView.as_view(), name='register-event'),
     path('event/<int:pk>/confirm', views.EventDetailView.as_view(), name='event-detail'),
]