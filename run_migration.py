#!/usr/bin/env python
"""
One-time migration script to run in Railway environment
This will run the PostgreSQL migrations and data loading
"""

import os
import sys
import django
from django.core.management import execute_from_command_line

def run_migration():
    """Run PostgreSQL migration and data loading"""
    
    # Set up Django environment
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wedding_site.settings')
    django.setup()
    
    print("🚀 Starting PostgreSQL migration...")
    
    try:
        # Step 1: Create tables
        print("📋 Creating PostgreSQL tables...")
        execute_from_command_line(['manage.py', 'migrate', '--run-syncdb'])
        
        # Step 2: Load data
        print("📥 Loading wedding data backup...")
        execute_from_command_line(['manage.py', 'loaddata', 'wedding_data_backup.json'])
        
        # Step 3: Verify
        print("🔍 Verifying migration...")
        from rsvp.models import Guest
        from django.contrib.auth.models import User
        
        guest_count = Guest.objects.count()
        user_count = User.objects.count()
        
        print(f"✅ Migration completed successfully!")
        print(f"   - Guests migrated: {guest_count}")
        print(f"   - Admin users: {user_count}")
        
        # Create a marker file to prevent re-running
        with open('/tmp/migration_completed', 'w') as f:
            f.write('Migration completed successfully')
            
        return True
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        return False

if __name__ == '__main__':
    # Only run if not already completed
    if not os.path.exists('/tmp/migration_completed'):
        run_migration()
    else:
        print("✅ Migration already completed")