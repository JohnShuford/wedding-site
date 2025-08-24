#!/usr/bin/env python
"""
Migration script to move from SQLite to PostgreSQL on Railway
"""

import os
import sys
import django
from django.core.management import execute_from_command_line

def migrate_to_postgres():
    """
    Migrate from SQLite to PostgreSQL
    """
    
    print("🗄️  Starting PostgreSQL migration...")
    
    # Set Django settings
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wedding_site.settings')
    django.setup()
    
    try:
        # Step 1: Run migrations to create tables
        print("📋 Creating PostgreSQL tables...")
        execute_from_command_line(['manage.py', 'migrate', '--run-syncdb'])
        
        # Step 2: Load data from backup
        print("📥 Loading data from backup...")
        execute_from_command_line(['manage.py', 'loaddata', 'wedding_data_backup.json'])
        
        print("✅ Migration completed successfully!")
        print("🔍 Verifying data...")
        
        # Quick verification
        from rsvp.models import Guest
        from wedding.models import StoryEntry
        from django.contrib.auth.models import User
        
        guest_count = Guest.objects.count()
        story_count = StoryEntry.objects.count() 
        user_count = User.objects.count()
        
        print(f"   - {guest_count} guests migrated")
        print(f"   - {story_count} story entries migrated") 
        print(f"   - {user_count} admin users migrated")
        
        return True
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        return False

if __name__ == '__main__':
    migrate_to_postgres()