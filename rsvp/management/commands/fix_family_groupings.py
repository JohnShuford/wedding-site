from django.core.management.base import BaseCommand
from rsvp.models import Guest
import uuid

class Command(BaseCommand):
    help = 'Fix family groupings and add new guests'

    def handle(self, *args, **options):
        self.stdout.write("🔧 Starting family groupings fix...")
        
        # Generate new group IDs
        liz_gary_group = uuid.uuid4()
        cliff_group = uuid.uuid4()
        verlie_group = uuid.uuid4()
        mary_anne_group = uuid.uuid4()
        mary_miller_group = uuid.uuid4()
        bone_family_group = uuid.uuid4()
        
        # John's existing group (Kelly will join this)
        john_kelly_group = "ae55b705-2ded-41ce-a356-0260cb8e941d"
        # Existing Lisa & Robert group (they keep this)
        lisa_robert_group = "28acc262-2231-4359-9164-2a3b60208653"
        
        try:
            # Fix existing Throckmorton family groupings
            self.stdout.write("👥 Fixing Throckmorton family groups...")
            
            # Kelly moves to John's group
            kelly = Guest.objects.get(first_name="Kelly", last_name="Throckmorton")
            kelly.group_id = john_kelly_group
            kelly.save()
            self.stdout.write(f"   ✅ Kelly moved to John's group")
            
            # Liz & Gary get new group
            liz = Guest.objects.get(first_name="Liz", last_name="Throckmorton")
            gary = Guest.objects.get(first_name="Gary", last_name="Throckmorton")
            liz.group_id = liz_gary_group
            gary.group_id = liz_gary_group
            liz.save()
            gary.save()
            self.stdout.write(f"   ✅ Liz & Gary grouped together")
            
            # Cliff gets his own group
            cliff = Guest.objects.get(first_name="Cliff", last_name="Throckmorton")
            cliff.group_id = cliff_group
            cliff.save()
            self.stdout.write(f"   ✅ Cliff in solo group")
            
            # Verlie gets her own group
            verlie = Guest.objects.get(first_name="Verlie", last_name="Throckmorton")
            verlie.group_id = verlie_group
            verlie.save()
            self.stdout.write(f"   ✅ Verlie in solo group")
            
            # Fix Miller family groupings
            self.stdout.write("👥 Fixing Miller family groups...")
            
            # Mary Anne gets her own group (Lisa & Robert keep existing group)
            mary_anne = Guest.objects.get(first_name="Mary Anne", last_name="Miller")
            mary_anne.group_id = mary_anne_group
            mary_anne.save()
            self.stdout.write(f"   ✅ Mary Anne in solo group")
            
            # Add new guests
            self.stdout.write("➕ Adding new guests...")
            
            # Mary Miller (solo)
            Guest.objects.create(
                group_id=mary_miller_group,
                first_name="Mary",
                last_name="Miller",
                email="mary.miller.new@placeholder.com"
            )
            self.stdout.write(f"   ✅ Added Mary Miller (solo)")
            
            # Bone family (all together)
            bone_members = [
                {"first_name": "Robyn", "email": "robyn.bone@placeholder.com"},
                {"first_name": "Tahajudd", "email": "tahajudd.bone@placeholder.com"},
                {"first_name": "Sophia", "email": "sophia.bone@placeholder.com"},
                {"first_name": "Reiley", "email": "reiley.bone@placeholder.com"},
            ]
            
            for member in bone_members:
                Guest.objects.create(
                    group_id=bone_family_group,
                    first_name=member["first_name"],
                    last_name="Bone",
                    email=member["email"]
                )
                self.stdout.write(f"   ✅ Added {member['first_name']} Bone")
            
            # Verify results
            self.stdout.write("🔍 Verifying groupings...")
            
            # Count groups
            john_kelly_count = Guest.objects.filter(group_id=john_kelly_group).count()
            liz_gary_count = Guest.objects.filter(group_id=liz_gary_group).count()
            cliff_count = Guest.objects.filter(group_id=cliff_group).count()
            verlie_count = Guest.objects.filter(group_id=verlie_group).count()
            lisa_robert_count = Guest.objects.filter(group_id=lisa_robert_group).count()
            mary_anne_count = Guest.objects.filter(group_id=mary_anne_group).count()
            mary_miller_count = Guest.objects.filter(group_id=mary_miller_group).count()
            bone_count = Guest.objects.filter(group_id=bone_family_group).count()
            
            self.stdout.write(f"   📊 John & Kelly group: {john_kelly_count} members")
            self.stdout.write(f"   📊 Liz & Gary group: {liz_gary_count} members")
            self.stdout.write(f"   📊 Cliff solo: {cliff_count} member")
            self.stdout.write(f"   📊 Verlie solo: {verlie_count} member")
            self.stdout.write(f"   📊 Lisa & Robert group: {lisa_robert_count} members")
            self.stdout.write(f"   📊 Mary Anne solo: {mary_anne_count} member")
            self.stdout.write(f"   📊 Mary Miller solo: {mary_miller_count} member")
            self.stdout.write(f"   📊 Bone family: {bone_count} members")
            
            total_guests = Guest.objects.count()
            self.stdout.write(f"✅ Family groupings fixed successfully! Total guests: {total_guests}")
            
        except Exception as e:
            self.stdout.write(f"❌ Error: {e}")
            raise e