# wedding/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('our-story/', views.our_story, name='our_story'),
    path('itinerary/', views.itinerary, name='itinerary'),
    path('rsvp/', views.rsvp, name='rsvp'),
    path('honeymoon-fund/', views.honeymoon_fund, name='honeymoon_fund'),
]

