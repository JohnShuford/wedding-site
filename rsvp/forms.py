from django import forms
from .models import Guest

class GuestLookupForm(forms.Form):
    first_name = forms.CharField(max_length=100, label='')
    last_name = forms.CharField(max_length=100, label='')

class RSVPDetailsForm(forms.ModelForm):
    class Meta:
        model = Guest
        fields = ['email', 'dietary_restrictions', 'message_for_couple']