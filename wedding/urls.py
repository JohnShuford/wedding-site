from django.urls import path, include
from . import views
from .views import StoryEntryViewSet
from django.conf import settings
from django.conf.urls.static import static

app_name = 'wedding'

urlpatterns = [
    path('', views.home, name='home'),
    path('our-story/', views.our_story, name='our_story'),
    path('itinerary/', views.itinerary, name='itinerary'),
    path('rsvp/', views.rsvp, name='rsvp'),
    path('honeymoon-fund/', views.honeymoon_fund, name='honeymoon_fund'),
    path('gallery/', views.gallery, name='gallery'),
    path('story-entries/', StoryEntryViewSet.as_view({'get': 'list'}), name='story_entries'),
    path('story-entries/<int:pk>/', StoryEntryViewSet.as_view({'get': 'retrieve'}), name='story_entry_detail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)