from .forms import GuestLookupForm
# from .forms import RSVPTypeForm
from .forms import RSVPDetailsForm
from .models import Guest
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, get_object_or_404

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
            group_guests = Guest.objects.filter(group_id=guest.group_id)
            if group_guests.count() == 1:
                return HttpResponseRedirect(reverse('rsvp_confirm_attendance', args=[guest.id]))
            else:
                return HttpResponseRedirect(reverse('confirm_group_attendance', args=[guest.group_id]))
        else:
            return HttpResponseRedirect(reverse('rsvp'))

    return render(request, 'rsvp/confirm_guest.html', {'guest': guest})
        
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

def confirm_group_attendance(request, group_id):
    guests = Guest.objects.filter(group_id=group_id)
    if not guests.exists():
        return HttpResponseRedirect(reverse('rsvp'))

    if request.method == 'POST':
        for guest in guests:
            attending = request.POST.get(f"attending_{guest.id}")
            if attending == 'yes':
                guest.attending = True
                guest.save()
                return HttpResponseRedirect(reverse('rsvp_questions_yes', args=[guest.id]))
            elif attending == 'no':
                guest.attending = False
                guest.save()
                return HttpResponseRedirect(reverse('rsvp_questions_no', args=[guest.id]))

    return render(request, 'rsvp/group_confirm.html', {'guests': guests})