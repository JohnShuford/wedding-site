from django.shortcuts import render

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