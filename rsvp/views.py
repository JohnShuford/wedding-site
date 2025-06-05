from .forms import GuestLookupForm
from .forms import RSVPTypeForm
from .forms import RSVPDetailsForm
from .models import Guest
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, get_object_or_404

def rsvp_start(request):
    if request.method == 'POST':
        form = RSVPTypeForm(request.POST)
        if form.is_valid():
            # Store in session so we can access later
            request.session['rsvp_type'] = form.cleaned_data['rsvp_type']
            return HttpResponseRedirect(reverse('rsvp'))
    else:
        form = RSVPTypeForm()

    return render(request, 'rsvp/rsvp_start.html', {'form': form})

def rsvp_entry_point(request):
    if request.method == 'POST':
        form = GuestLookupForm(request.POST)
        if form.is_valid():
            first = form.cleaned_data['first_name'].strip()
            last = form.cleaned_data['last_name'].strip()
            matches = Guest.objects.filter(first_name__iexact=first, last_name__iexact=last)

            if not matches.exists():
                return render(request, 'rsvp/not_found.html', {'form': form})

            if matches.count() == 1:
                guest = matches.first()
                return render(request, 'rsvp/confirm_guest.html', {'guest': guest})

            return render(request, 'rsvp/select_guest.html', {'matches': matches})
    else:
        form = GuestLookupForm()

    return render(request, 'rsvp/lookup.html', {'form': form})

def confirm_guest(request, guest_id):
    guest = get_object_or_404(Guest, pk=guest_id)
    if request.method == 'POST':
        confirm = request.POST.get('confirm')
        if confirm == 'yes':
            return HttpResponseRedirect(reverse('rsvp_questions', args=[guest.id]))
        else:
            return render(request, 'rsvp/not_found.html', {'form': GuestLookupForm()})
        
# RSVP Confirm Page - Choose Yes or No

def rsvp_confirm_attendance(request, guest_id):
    guest = get_object_or_404(Guest, pk=guest_id)
    if request.method == 'POST':
        attending = request.POST.get('attending')
        if attending == 'yes':
            guest.attending = True
            guest.save()
            return HttpResponseRedirect(reverse('rsvp_questions_yes', args=[guest.id]))
        elif attending == 'no':
            guest.attending = False
            guest.save()
            return HttpResponseRedirect(reverse('rsvp_questions_no', args=[guest.id]))
    return render(request, 'rsvp/rsvp_confirm.html', {'guest': guest})

# RSVP Questions - Yes Flow

def rsvp_questions_yes(request, guest_id):
    guest = get_object_or_404(Guest, pk=guest_id)
    if request.method == 'POST':
        form = RSVPDetailsForm(request.POST, instance=guest)
        if form.is_valid():
            form.save()
            return render(request, 'rsvp/thank_you.html', {'guest': guest})
    else:
        form = RSVPDetailsForm(instance=guest)
    return render(request, 'rsvp/rsvp_questions_yes.html', {'form': form, 'guest': guest})

# RSVP Questions - No Flow

def rsvp_questions_no(request, guest_id):
    guest = get_object_or_404(Guest, pk=guest_id)
    if request.method == 'POST':
        form = RSVPDetailsForm(request.POST, instance=guest)
        if form.is_valid():
            form.save()
            return render(request, 'rsvp/thank_you.html', {'guest': guest})
    else:
        form = RSVPDetailsForm(instance=guest)
    return render(request, 'rsvp/rsvp_questions_no.html', {'form': form, 'guest': guest})
