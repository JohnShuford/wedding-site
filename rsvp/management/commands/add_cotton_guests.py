from django.core.management.base import BaseCommand
from rsvp.models import Guest
import uuid

class Command(BaseCommand):
    help = 'Add Will Cotton and J.T. Cotton as individual guests'

    def handle(self, *args, **options):
        self.stdout.write("Adding Cotton family guests...")

        # Show current guest count
        self.stdout.write("Current guest count: {}".format(Guest.objects.count()))

        # Add individual guests with separate group IDs
        cotton_guests = [
            ("Will", "Cotton"),
            ("J.T.", "Cotton"),
        ]

        for first, last in cotton_guests:
            # Check if guest already exists
            if not Guest.objects.filter(first_name=first, last_name=last).exists():
                # Create guest with unique group ID
                Guest.objects.create(
                    first_name=first,
                    last_name=last,
                    email='placeholder@example.com',
                    group_id=uuid.uuid4()
                )
                self.stdout.write(self.style.SUCCESS(f"✓ Added new guest: {first} {last}"))
            else:
                self.stdout.write(self.style.WARNING(f"⚠ Guest already exists: {first} {last}"))

        self.stdout.write(self.style.SUCCESS("Cotton guests added successfully!"))
        self.stdout.write("Final guest count: {}".format(Guest.objects.count()))
