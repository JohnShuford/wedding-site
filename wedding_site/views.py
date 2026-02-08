from django.shortcuts import render


def home(request):
    return render(request, 'home.html')

def our_story(request):
    return render(request, 'our_story.html')

def itinerary(request):
    return render(request, 'itinerary.html')

def gallery(request):
    return render(request, 'gallery.html')

def honeymoon_fund(request):
    return render(request, 'honeymoon_fund.html')

def downtown_westminster(request):
    return render(request, 'downtown_westminster.html')

def faq(request):
    return render(request, 'faq.html')