from django.core.management.base import BaseCommand
from rsvp.models import Guest
import uuid

class Command(BaseCommand):
    help = 'Update guest names and groups for wedding launch'

    def handle(self, *args, **options):
        self.stdout.write("Starting guest database updates...")
        
        # First, let's backup and show current data
        self.stdout.write("Current guest count: {}".format(Guest.objects.count()))
        
        # Name corrections - First names only
        first_name_updates = [
            ("Jennie", "Jennifer"),
            ("Mary Anne", "Mary Ann"), 
            ("Steph", "Stephanie"),
            ("Al", "Albert"),
            ("Bev", "Beverly"),
            ("Delbert", "Del"),
        ]
        
        for old_name, new_name in first_name_updates:
            guests = Guest.objects.filter(first_name=old_name)
            if guests.exists():
                count = guests.update(first_name=new_name)
                self.stdout.write(f"Updated {count} guest(s): {old_name} → {new_name}")
            else:
                self.stdout.write(f"No guests found with first name: {old_name}")
        
        # Last name corrections
        last_name_updates = [
            ("William", "Woodrich", "Wodrich"),
            ("Caley", "Obrien", "O'Brien"),
            ("Cissy", "Shuford", "Koford"),
        ]
        
        for first_name, old_last, new_last in last_name_updates:
            guests = Guest.objects.filter(first_name=first_name, last_name=old_last)
            if guests.exists():
                count = guests.update(last_name=new_last)
                self.stdout.write(f"Updated {count} guest(s): {first_name} {old_last} → {first_name} {new_last}")
            else:
                self.stdout.write(f"No guests found: {first_name} {old_last}")
        
        # Handle Kelly and John bride/groom group
        kelly = Guest.objects.filter(first_name="Kelly", last_name="Throckmorton").first()
        john = Guest.objects.filter(first_name="John", last_name="Shuford").first()
        
        if kelly and john:
            # Create new group ID for bride and groom
            bride_groom_group = uuid.uuid4()
            kelly.group_id = bride_groom_group
            john.group_id = bride_groom_group
            kelly.save()
            john.save()
            self.stdout.write(f"Created bride & groom group: Kelly Throckmorton + John Shuford")
        else:
            self.stdout.write("Could not find Kelly Throckmorton or John Shuford")
        
        # Split Cliff and Verlie into separate IDs
        cliff = Guest.objects.filter(first_name="Cliff").first()
        verlie = Guest.objects.filter(first_name="Verlie").first()
        
        if cliff and verlie and cliff.group_id == verlie.group_id:
            # Give Verlie a new group ID
            verlie.group_id = uuid.uuid4()
            verlie.save()
            self.stdout.write("Split Cliff and Verlie into separate groups")
        
        # Add new guests
        # Create single group ID for Bone family
        bone_family_group = uuid.uuid4()
        
        bone_family = [
            ("Robyn", "Bone"),
            ("Tahajudd", "Bone"),
            ("Sophia", "Bone"),
            ("Reiley", "Bone"),
        ]
        
        for first, last in bone_family:
            if not Guest.objects.filter(first_name=first, last_name=last).exists():
                Guest.objects.create(
                    first_name=first,
                    last_name=last,
                    email=f"{first.lower()}@example.com",
                    group_id=bone_family_group
                )
                self.stdout.write(f"Added new guest to Bone family: {first} {last}")
            else:
                self.stdout.write(f"Guest already exists: {first} {last}")
        
        # Add individual guests
        individual_guests = [
            ("Mary", "Miller"),
            ("Damelys", "Marin"),
        ]
        
        for first, last in individual_guests:
            if not Guest.objects.filter(first_name=first, last_name=last).exists():
                Guest.objects.create(
                    first_name=first,
                    last_name=last,
                    email=f"{first.lower()}@example.com",
                    group_id=uuid.uuid4()
                )
                self.stdout.write(f"Added new individual guest: {first} {last}")
            else:
                self.stdout.write(f"Guest already exists: {first} {last}")
        
        self.stdout.write("Guest updates completed!")
        self.stdout.write("Final guest count: {}".format(Guest.objects.count()))