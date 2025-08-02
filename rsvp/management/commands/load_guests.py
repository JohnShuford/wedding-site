import csv
import uuid
from django.core.management.base import BaseCommand
from django.db import transaction
from rsvp.models import Guest


class Command(BaseCommand):
    help = 'Load guests from CSV file and add test guests'

    def add_arguments(self, parser):
        parser.add_argument(
            '--csv-path',
            type=str,
            default='/Users/airforce/Desktop/Guest List.csv',
            help='Path to the guest list CSV file'
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing guests before loading'
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('Clearing existing guests...')
            Guest.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Existing guests cleared.'))

        # Define family groupings with UUIDs
        family_groups = self.get_family_groups()
        
        # Load real guests from CSV
        self.load_real_guests(options['csv_path'], family_groups)
        
        # Add test guests
        self.add_test_guests()
        
        # Final summary
        total_guests = Guest.objects.count()
        self.stdout.write(
            self.style.SUCCESS(f'Successfully loaded {total_guests} guests total.')
        )

    def get_family_groups(self):
        """Define all family groupings with pre-generated UUIDs"""
        return {
            'throckmorton': {
                'uuid': uuid.uuid4(),
                'members': ['Kelly Throckmorton', 'Liz Throckmorton', 'Gary Throckmorton', 
                           'Cliff Throckmorton', 'Verlie Throckmorton']
            },
            'throckmorton_michaud': {
                'uuid': uuid.uuid4(),
                'members': ['Sarah Throckmorton-Michaud', 'Taylor Throckmorton-Michaud']
            },
            'padgett': {
                'uuid': uuid.uuid4(),
                'members': ['Kathy Padgett', 'Bobby Padgett']
            },
            'ondrasek': {
                'uuid': uuid.uuid4(),
                'members': ['Jane Ondrasek', 'Robert Ondrasek']
            },
            'miller': {
                'uuid': uuid.uuid4(),
                'members': ['Lisa Miller', 'Robert Miller', 'Mary Anne Miller']
            },
            'shuford_1': {
                'uuid': uuid.uuid4(),
                'members': ['Al Shuford', 'Bev Shuford']
            },
            'shuford_2': {
                'uuid': uuid.uuid4(),
                'members': ['Delbert Shuford', 'Cissy Shuford']
            },
            'shuford_3': {
                'uuid': uuid.uuid4(),
                'members': ['Steph Shuford', 'Asher McDonald', 'Quinn McDonald']
            },
            'calander_1': {
                'uuid': uuid.uuid4(),
                'members': ['Shirley Calander', 'Dennis Calander', 'Paul Calander']
            },
            'calander_2': {
                'uuid': uuid.uuid4(),
                'members': ['Dusti Calander', 'Jennie Whiffin']
            },
            'rogers': {
                'uuid': uuid.uuid4(),
                'members': ['Rachel Rogers', 'Steven Rogers']
            },
            'rubino_2': {
                'uuid': uuid.uuid4(),
                'members': ['Shelby Rubino', 'William Woodrich']
            },
            'collins_grote': {
                'uuid': uuid.uuid4(),
                'members': ['Molly Collins', 'Jacob Grote']
            },
            'erlandson_kenny': {
                'uuid': uuid.uuid4(),
                'members': ['Maria Erlandson', 'Kenny Kenny']
            },
            'pereira': {
                'uuid': uuid.uuid4(),
                'members': ['Lauren Pereira', 'Gabe Pereira']
            },
            'fink': {
                'uuid': uuid.uuid4(),
                'members': ['Rachel Fink', 'Mike Fink']
            }
        }

    def find_guest_family(self, first_name, last_name, family_groups):
        """Find which family group a guest belongs to"""
        full_name = f"{first_name} {last_name}"
        
        for family_key, family_data in family_groups.items():
            if full_name in family_data['members']:
                return family_data['uuid']
        
        # Individual guests get their own UUID
        return uuid.uuid4()

    def load_real_guests(self, csv_path, family_groups):
        """Load real guests from CSV file"""
        self.stdout.write(f'Loading guests from {csv_path}...')
        
        with transaction.atomic():
            with open(csv_path, 'r', encoding='utf-8-sig') as file:
                reader = csv.DictReader(file)
                real_guests_created = 0
                
                for row in reader:
                    first_name = row['First Name'].strip()
                    last_name = row['Last Name'].strip()
                    
                    # Find family group UUID
                    group_id = self.find_guest_family(first_name, last_name, family_groups)
                    
                    guest, created = Guest.objects.get_or_create(
                        first_name=first_name,
                        last_name=last_name,
                        defaults={'group_id': group_id}
                    )
                    
                    if created:
                        real_guests_created += 1
                        self.stdout.write(f'  Added: {first_name} {last_name}')
                    else:
                        self.stdout.write(f'  Exists: {first_name} {last_name}')
        
        self.stdout.write(
            self.style.SUCCESS(f'Loaded {real_guests_created} real guests from CSV.')
        )

    def add_test_guests(self):
        """Add test guests with NATO phonetic alphabet + pop culture names"""
        self.stdout.write('Adding test guests...')
        
        test_guests_data = [
            # Individual test guests
            {'first_name': 'Alpha', 'last_name': 'Pitt', 'group_id': uuid.uuid4()},
            {'first_name': 'Bravo', 'last_name': 'Aniston', 'group_id': uuid.uuid4()},
            {'first_name': 'Charlie', 'last_name': 'Jolie', 'group_id': uuid.uuid4()},
            {'first_name': 'Delta', 'last_name': 'Cruise', 'group_id': uuid.uuid4()},
            
            # Test Family A (2 members) - Clooney family
            {'first_name': 'Echo', 'last_name': 'Clooney', 'group_id': None, 'family': 'clooney'},
            {'first_name': 'Foxtrot', 'last_name': 'Clooney', 'group_id': None, 'family': 'clooney'},
            
            # Test Family B (3 members) - Hanks family  
            {'first_name': 'Golf', 'last_name': 'Hanks', 'group_id': None, 'family': 'hanks'},
            {'first_name': 'Hotel', 'last_name': 'Hanks', 'group_id': None, 'family': 'hanks'},
            {'first_name': 'India', 'last_name': 'Hanks', 'group_id': None, 'family': 'hanks'},
            
            # Test Family C (4 members) - Streep family
            {'first_name': 'Juliet', 'last_name': 'Streep', 'group_id': None, 'family': 'streep'},
            {'first_name': 'Kilo', 'last_name': 'Streep', 'group_id': None, 'family': 'streep'},
            {'first_name': 'Lima', 'last_name': 'Streep', 'group_id': None, 'family': 'streep'},
            {'first_name': 'Mike', 'last_name': 'Streep', 'group_id': None, 'family': 'streep'},
        ]
        
        # Generate family group IDs
        family_uuids = {
            'clooney': uuid.uuid4(),
            'hanks': uuid.uuid4(),
            'streep': uuid.uuid4(),
        }
        
        with transaction.atomic():
            test_guests_created = 0
            
            for guest_data in test_guests_data:
                # Assign family group ID if part of a family
                if 'family' in guest_data:
                    guest_data['group_id'] = family_uuids[guest_data['family']]
                    del guest_data['family']
                
                guest, created = Guest.objects.get_or_create(
                    first_name=guest_data['first_name'],
                    last_name=guest_data['last_name'],
                    defaults={'group_id': guest_data['group_id']}
                )
                
                if created:
                    test_guests_created += 1
                    self.stdout.write(f'  Added test guest: {guest_data["first_name"]} {guest_data["last_name"]}')
        
        self.stdout.write(
            self.style.SUCCESS(f'Added {test_guests_created} test guests.')
        )