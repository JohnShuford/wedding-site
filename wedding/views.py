import os
from django.conf import settings
from django.shortcuts import render
from rest_framework import viewsets
from .models import StoryEntry
from .serializers import StoryEntrySerializer
class StoryEntryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = StoryEntry.objects.all()
    serializer_class = StoryEntrySerializer

def home(request):
    return render(request, 'wedding/home.html')

def our_story(request):
    entries = StoryEntry.objects.all().order_by('date')
    return render(request, 'wedding/our_story.html', {
        'story_entries': entries
    })

def itinerary(request):
    return render(request, 'wedding/itinerary.html')

def rsvp(request):
    return render(request, 'wedding/rsvp.html')

def gallery(request):
    albums = [
        {'slug': 'denver-botanic-gardens', 'name': 'Denver Botanic Gardens'},
        {'slug': 'telluride', 'name': 'Telluride'},
        {'slug': 'wedding', 'name': 'Wedding'},
    ]
    gallery_base = os.path.join(settings.BASE_DIR, 'wedding', 'static', 'images', 'gallery')
    for album in albums:
        album_dir = os.path.join(gallery_base, album['slug'])
        if os.path.isdir(album_dir):
            album['photos'] = sorted([
                f for f in os.listdir(album_dir)
                if f.lower().endswith(('.jpg', '.jpeg'))
            ])
        else:
            album['photos'] = []
    return render(request, 'wedding/gallery.html', {'albums': albums})

def honeymoon_fund(request):
    return render(request, 'wedding/honeymoon_fund.html')

def downtown_westminster(request):
    return render(request, 'wedding/downtown_westminster.html')

def faq(request):
    return render(request, 'wedding/faq.html')

