from django import forms
from django.core.validators import EmailValidator
from django.utils.safestring import mark_safe
from .models import Guest

class GuestLookupForm(forms.Form):
    first_name = forms.CharField(max_length=100, label='')
    last_name = forms.CharField(max_length=100, label='')

class RSVPDetailsForm(forms.ModelForm):
    class Meta:
        model = Guest
        fields = ['email', 'dietary_restrictions', 'message_for_couple']
        widgets = {
            'email': forms.EmailInput(attrs={
                'placeholder': 'your.email@example.com',
                'class': 'form-control',
                'required': True
            }),
            'dietary_restrictions': forms.Textarea(attrs={
                'placeholder': 'Any dietary restrictions or allergies we should know about?',
                'rows': 3,
                'class': 'form-control'
            }),
            'message_for_couple': forms.Textarea(attrs={
                'placeholder': 'Share your excitement, memories, or well wishes with Kelly & John!',
                'rows': 4,
                'class': 'form-control'
            })
        }
        labels = {
            'email': mark_safe('Email Address * <span class="email-note">(so we can send you photos!)</span>'),
            'dietary_restrictions': 'Dietary Restrictions',
            'message_for_couple': 'Message for the Couple'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ensure email is required
        self.fields['email'].required = True
        self.fields['email'].validators.append(EmailValidator())
        
        # Add help text
        self.fields['email'].help_text = 'Required for event updates and photos'
        
    def clean_email(self):
        """Custom email validation with helpful error messages"""
        email = self.cleaned_data.get('email')
        if not email:
            raise forms.ValidationError('Email address is required.')
        
        # Django's EmailField already validates format, but we can add custom logic here
        return email.lower().strip()