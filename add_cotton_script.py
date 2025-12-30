#!/usr/bin/env python
"""
Standalone script to add Will Cotton and J.T. Cotton to the guest database.
Run with: railway run python add_cotton_script.py
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wedding_site.settings')
django.setup()

from rsvp.models import Guest
import uuid

def main():
    print("Adding Cotton family guests...")
    print(f"Current guest count: {Guest.objects.count()}")

    # Add individual guests with separate group IDs
    cotton_guests = [
        ("Will", "Cotton"),
        ("J.T.", "Cotton"),
    ]

    for first, last in cotton_guests:
        # Check if guest already exists
        if not Guest.objects.filter(first_name=first, last_name=last).exists():
            # Create guest with unique group ID
            new_guest = Guest.objects.create(
                first_name=first,
                last_name=last,
                email='placeholder@example.com',
                group_id=uuid.uuid4()
            )
            print(f"✓ Added new guest: {first} {last} (Group ID: {new_guest.group_id})")
        else:
            guest = Guest.objects.get(first_name=first, last_name=last)
            print(f"⚠ Guest already exists: {first} {last} (Group ID: {guest.group_id})")

    print("\nCotton guests added successfully!")
    print(f"Final guest count: {Guest.objects.count()}")

if __name__ == '__main__':
    main()
