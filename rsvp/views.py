from .forms import GuestLookupForm
from .forms import RSVPDetailsForm
from .models import Guest
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from django.contrib import messages

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

def rsvp_questions_yes(request, guest_id):
    guest = get_object_or_404(Guest, pk=guest_id)
    if request.method == 'POST':
        form = RSVPDetailsForm(request.POST, instance=guest)
        if form.is_valid():
            form.save()
            # For single guests, pass as single guest
            return render(request, 'rsvp/thank_you.html', {'guest': guest})
    else:
        form = RSVPDetailsForm(instance=guest)
    return render(request, 'rsvp/rsvp_questions_yes.html', {'form': form, 'guest': guest})

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
        # Process all guests in the group
        attending_guests = []
        not_attending_guests = []
        
        for guest in guests:
            attending = request.POST.get(f"attending_{guest.id}")
            if attending == 'yes':
                guest.attending = True
                attending_guests.append(guest)
            elif attending == 'no':
                guest.attending = False
                not_attending_guests.append(guest)
            guest.save()
        
        # No need to store in session since we pass group_id in URL
        
        # Redirect based on who's attending
        if attending_guests and not_attending_guests:
            # Mixed group - some attending, some not
            return HttpResponseRedirect(reverse('group_rsvp_questions', args=[group_id]))
        elif attending_guests:
            # Everyone attending
            return HttpResponseRedirect(reverse('group_rsvp_questions', args=[group_id]))
        else:
            # All guests declined
            return HttpResponseRedirect(reverse('group_declined', args=[group_id]))

    return render(request, 'rsvp/group_confirm.html', {'guests': guests})

def group_rsvp_questions(request, group_id):
    """Handle RSVP questions for all attending guests in a group"""
    guests = Guest.objects.filter(group_id=group_id)
    attending_guests = guests.filter(attending=True)
    not_attending_guests = guests.filter(attending=False)
    
    if not attending_guests.exists():
        return HttpResponseRedirect(reverse('group_declined', args=[group_id]))
    
    if request.method == 'POST':
        all_forms_valid = True
        forms = {}
        
        # Create and validate forms for all attending guests
        for guest in attending_guests:
            form = RSVPDetailsForm(request.POST, instance=guest, prefix=str(guest.id))
            forms[guest.id] = form
            if not form.is_valid():
                all_forms_valid = False
        
        # Handle declined guests' contact info
        for guest in not_attending_guests:
            email = request.POST.get(f"email_{guest.id}")
            message = request.POST.get(f"message_{guest.id}")
            if email:
                guest.email = email
            if message:
                guest.message = message
            guest.save()
        
        if all_forms_valid:
            # Save all attending guest forms
            for guest_id, form in forms.items():
                form.save()
            return HttpResponseRedirect(reverse('group_thank_you', args=[group_id]))
    else:
        # Create forms for GET request
        forms = {}
        for guest in attending_guests:
            forms[guest.id] = RSVPDetailsForm(instance=guest, prefix=str(guest.id))
    
    # Pair attending guests with their forms for template
    attending_guest_forms = [(guest, forms[guest.id]) for guest in attending_guests]
    
    return render(request, 'rsvp/group_rsvp_questions.html', {
        'attending_guest_forms': attending_guest_forms,
        'not_attending_guests': not_attending_guests,
        'group_id': group_id
    })

def group_declined(request, group_id):
    """Page for when all group members decline"""
    guests = Guest.objects.filter(group_id=group_id, attending=False)
    
    if request.method == 'POST':
        # Process any optional contact info they want to provide
        for guest in guests:
            email = request.POST.get(f"email_{guest.id}")
            message = request.POST.get(f"message_{guest.id}")
            if email:
                guest.email = email
            if message:
                guest.message = message
            guest.save()
        
        return HttpResponseRedirect(reverse('group_thank_you', args=[group_id]))
    
    return render(request, 'rsvp/group_declined.html', {'guests': guests, 'group_id': group_id})

def group_thank_you(request, group_id):
    """Thank you page for group RSVPs"""
    guests = Guest.objects.filter(group_id=group_id)
    return render(request, 'rsvp/group_thank_you.html', {'guests': guests, 'group_id': group_id})