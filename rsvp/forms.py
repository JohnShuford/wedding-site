from django import forms
from .models import Guest

class GuestLookupForm(forms.Form):
    first_name = forms.CharField(max_length=100, label='First Name')
    last_name = forms.CharField(max_length=100, label='Last Name')

# class RSVPTypeForm(forms.Form):
#     RSVP_CHOICES = [
#         ('solo', 'Just Myself'),
#         ('group', 'Myself and Others'),
#     ]
#     rsvp_type = forms.ChoiceField(
#         choices=RSVP_CHOICES,
#         widget=forms.RadioSelect,
#         label="Who would you like to RSVP for?"
#     )

class RSVPDetailsForm(forms.ModelForm):
    class Meta:
        model = Guest
        fields = ['email', 'dietary_restrictions', 'message_for_couple']