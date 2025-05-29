from django.shortcuts import render

def rsvp_entry_point(request):
    return render(request, 'rsvp/index.html')
