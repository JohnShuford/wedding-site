"""Data migration: update StoryEntry image values from local paths to Cloudinary public_ids."""
import re
from django.db import migrations


# Mapping from local filenames (before Django's dedup suffix) to Cloudinary public_ids
CLOUDINARY_MAP = {
    'blueMoon': 'wedding-site/our-story/blueMoon',
    'RMNP': 'wedding-site/our-story/RMNP',
    'coSprings': 'wedding-site/our-story/coSprings',
    'leafPeeping': 'wedding-site/our-story/leafPeeping',
    'broncos': 'wedding-site/our-story/broncos',
    'oneYear': 'wedding-site/our-story/oneYear',
    '14er': 'wedding-site/our-story/14er',
    'mexico': 'wedding-site/our-story/mexico',
    'skiing': 'wedding-site/our-story/skiing',
    'twoYear': 'wedding-site/our-story/twoYear',
    'newZealand': 'wedding-site/our-story/newZealand',
    'threeYear': 'wedding-site/our-story/threeYear',
    'redRocks': 'wedding-site/our-story/redRocks',
    'nye': 'wedding-site/our-story/nye',
    'fourYear': 'wedding-site/our-story/fourYear',
    'engagement': 'wedding-site/our-story/engagement',
}


def forwards(apps, schema_editor):
    StoryEntry = apps.get_model('wedding', 'StoryEntry')
    for entry in StoryEntry.objects.all():
        old_value = str(entry.image)
        # Extract base name: "our_story_photos/blueMoon_618PL2O.png" -> "blueMoon"
        filename = old_value.split('/')[-1]           # "blueMoon_618PL2O.png"
        name_no_ext = filename.rsplit('.', 1)[0]      # "blueMoon_618PL2O"
        # Strip Django's 7-char dedup suffix
        base_name = re.sub(r'_[A-Za-z0-9]{7}$', '', name_no_ext)

        if base_name in CLOUDINARY_MAP:
            entry.image = CLOUDINARY_MAP[base_name]
            entry.save(update_fields=['image'])
            print(f"  Migrated: {old_value} -> {CLOUDINARY_MAP[base_name]}")
        else:
            print(f"  WARNING: No mapping for {old_value} (base: {base_name})")


def backwards(apps, schema_editor):
    # Not reversible - would need original filenames with dedup suffixes
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('wedding', '0003_alter_storyentry_image'),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
