#!/usr/bin/env python
"""
Migration script for Railway environment.
Runs Django migrations on startup.
"""

import os
import django
from django.core.management import execute_from_command_line


def run_migration():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wedding_site.settings')
    django.setup()

    print("Running migrations...")
    execute_from_command_line(['manage.py', 'migrate', '--run-syncdb'])
    print("Migrations complete.")

    # Load story entries fixture if the table is empty
    from wedding.models import StoryEntry
    if StoryEntry.objects.count() == 0:
        print("No story entries found — loading fixture...")
        execute_from_command_line(['manage.py', 'loaddata', 'wedding/fixtures/story_entries_backup.json'])
        print(f"Loaded {StoryEntry.objects.count()} story entries.")
    else:
        print(f"Story entries already exist ({StoryEntry.objects.count()}), skipping fixture load.")


if __name__ == '__main__':
    run_migration()
