from django.urls import path
from . import views

urlpatterns = [
    path('', views.rsvp_entry_point, name='rsvp'),
]