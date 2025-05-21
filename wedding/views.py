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
    return render(request, 'wedding/our_story.html')

def itinerary(request):
    return render(request, 'wedding/itinerary.html')

def rsvp(request):
    return render(request, 'wedding/rsvp.html')

def honeymoon_fund(request):
    return render(request, 'wedding/honeymoon_fund.html')

def gallery(request):
    return render(request, 'wedding/gallery.html')

def our_story(request):
    entries = StoryEntry.objects.all()
    return render(request, 'wedding/our_story.html', {
        'story_entries': entries
    })

print('Hello World')
print(StoryEntry.objects.all())
