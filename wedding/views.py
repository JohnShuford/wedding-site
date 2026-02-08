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

def gallery(request):
    albums = [
        {
            'slug': 'denver-botanic-gardens',
            'name': 'Denver Botanic Gardens',
            'photos': [
                'Kelly_and_John-4', 'Kelly_and_John-5', 'Kelly_and_John-11',
                'Kelly_and_John-13', 'Kelly_and_John-17', 'Kelly_and_John-22',
                'Kelly_and_John-23', 'Kelly_and_John-30', 'Kelly_and_John-31',
                'Kelly_and_John-41', 'Kelly_and_John-44', 'Kelly_and_John-47',
                'Kelly_and_John-55', 'Kelly_and_John-59', 'Kelly_and_John-62',
                'Kelly_and_John-63', 'Kelly_and_John-67', 'Kelly_and_John-76',
                'Kelly_and_John-81', 'Kelly_and_John-82', 'Kelly_and_John-85',
                'Kelly_and_John-87', 'Kelly_and_John-89', 'Kelly_and_John-94',
                'Kelly_and_John-99', 'Kelly_and_John-102', 'Kelly_and_John-106',
                'Kelly_and_John-112', 'Kelly_and_John-115', 'Kelly_and_John-125',
                'Kelly_and_John-126', 'Kelly_and_John-143', 'Kelly_and_John-146',
                'Kelly_and_John-150', 'Kelly_and_John-152', 'Kelly_and_John-154',
                'Kelly_and_John-162', 'Kelly_and_John-167', 'Kelly_and_John-169',
                'Kelly_and_John-174', 'Kelly_and_John-179', 'Kelly_and_John-182',
            ],
        },
        {
            'slug': 'telluride',
            'name': 'Telluride',
            'photos': [
                'K_and_J_1', 'K_and_J_2', 'K_and_J_3', 'K_and_J_4', 'K_and_J_5',
                'K_and_J_6', 'K_and_J_7', 'K_and_J_8', 'K_and_J_9', 'K_and_J_10',
                'K_and_J_11', 'K_and_J_12', 'K_and_J_13', 'K_and_J_14', 'K_and_J_15',
                'K_and_J_16', 'K_and_J_17', 'K_and_J_18', 'K_and_J_19', 'K_and_J_20',
                'K_and_J_21', 'K_and_J_22', 'K_and_J_23', 'K_and_J_24', 'K_and_J_25',
                'K_and_J_26', 'K_and_J_27', 'K_and_J_28', 'K_and_J_29', 'K_and_J_30',
                'K_and_J_31', 'K_and_J_32', 'K_and_J_33', 'K_and_J_34', 'K_and_J_35',
                'K_and_J_36', 'K_and_J_37', 'K_and_J_38', 'K_and_J_39', 'K_and_J_40',
                'K_and_J_41', 'K_and_J_42',
            ],
        },
        {
            'slug': 'wedding',
            'name': 'Wedding',
            'photos': [],
        },
    ]
    return render(request, 'wedding/gallery.html', {'albums': albums})

def honeymoon_fund(request):
    return render(request, 'wedding/honeymoon_fund.html')

def downtown_westminster(request):
    return render(request, 'wedding/downtown_westminster.html')

def faq(request):
    return render(request, 'wedding/faq.html')

