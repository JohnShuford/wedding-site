#!/usr/bin/env python
import os
import django
import re

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wedding_site.settings')
django.setup()

from rsvp.models import Guest

def clean_name_for_email(name):
    """Convert name to lowercase, remove special chars, replace spaces with dots"""
    # Remove special characters and convert to lowercase
    cleaned = re.sub(r'[^a-zA-Z\s-]', '', name.lower())
    # Replace spaces and hyphens with dots
    cleaned = re.sub(r'[\s-]+', '.', cleaned)
    # Remove leading/trailing dots
    cleaned = cleaned.strip('.')
    return cleaned

def create_placeholder_email(first_name, last_name):
    """Create placeholder email from first and last name"""
    first = clean_name_for_email(first_name)
    last = clean_name_for_email(last_name)
    return f"{first}.{last}@placeholder.com"

# Get all guests with empty emails
guests_without_emails = Guest.objects.filter(email='')
print(f"Found {guests_without_emails.count()} guests without emails")

updated_count = 0
for guest in guests_without_emails:
    placeholder_email = create_placeholder_email(guest.first_name, guest.last_name)
    guest.email = placeholder_email
    guest.save()
    print(f"Updated {guest.first_name} {guest.last_name} -> {placeholder_email}")
    updated_count += 1

print(f"\nSuccessfully updated {updated_count} guest emails with placeholders")