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


if __name__ == '__main__':
    run_migration()
