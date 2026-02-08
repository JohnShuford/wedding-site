#!/usr/bin/env python
"""Re-upload gallery photos with sanitized filenames (& -> _and_)."""

import os, sys, json
from pathlib import Path
from io import BytesIO

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wedding_site.settings')

import django
django.setup()

from django.conf import settings
from PIL import Image
import cloudinary, cloudinary.uploader

cloudinary.config(
    cloud_name=settings.CLOUDINARY_STORAGE['CLOUD_NAME'],
    api_key=settings.CLOUDINARY_STORAGE['API_KEY'],
    api_secret=settings.CLOUDINARY_STORAGE['API_SECRET'],
)

STATIC = PROJECT_ROOT / 'wedding' / 'static'

manifest_path = PROJECT_ROOT / 'scripts' / 'cloudinary_manifest.json'
with open(manifest_path) as f:
    manifest = json.load(f)

galleries = [
    ('images/gallery/denver-botanic-gardens', 'wedding-site/gallery/denver-botanic-gardens', 2000, 82),
    ('images/gallery/telluride', 'wedding-site/gallery/telluride', 2000, 82),
]

for local_dir, cloud_folder, max_width, quality in galleries:
    full_path = STATIC / local_dir
    files = sorted(f for f in full_path.iterdir() if f.is_file() and f.suffix.lower() in {'.jpg', '.jpeg'})
    print(f'\n[{cloud_folder}]')
    total_orig = 0
    total_comp = 0

    for filepath in files:
        public_id = filepath.stem.replace('&', '_and_')

        img = Image.open(filepath)
        if img.width > max_width:
            ratio = max_width / img.width
            img = img.resize((max_width, int(img.height * ratio)), Image.LANCZOS)
        if img.mode in ('RGBA', 'LA', 'P'):
            img = img.convert('RGB')

        buf = BytesIO()
        img.save(buf, format='JPEG', quality=quality, optimize=True)
        buf.seek(0)

        orig_size = os.path.getsize(filepath)
        comp_size = buf.getbuffer().nbytes
        total_orig += orig_size
        total_comp += comp_size

        result = cloudinary.uploader.upload(
            buf, folder=cloud_folder, public_id=public_id,
            overwrite=True, resource_type='image'
        )

        orig_mb = orig_size / (1024 * 1024)
        comp_kb = comp_size / 1024
        print(f'  {filepath.name}: {orig_mb:.1f} MB -> {comp_kb:.0f} KB | {result["secure_url"]}')

        manifest[f'{local_dir}/{filepath.name}'] = {
            'public_id': result['public_id'],
            'url': result['secure_url'],
            'format': result['format'],
            'width': result['width'],
            'height': result['height'],
            'bytes': result['bytes'],
            'original_filename': filepath.name,
        }

    reduction = (1 - total_comp / total_orig) * 100 if total_orig > 0 else 0
    print(f'  Subtotal: {total_orig / (1024*1024):.1f} MB -> {total_comp / (1024*1024):.1f} MB ({reduction:.0f}% reduction)')

with open(manifest_path, 'w') as f:
    json.dump(manifest, f, indent=2)

print(f'\nManifest updated: {len(manifest)} total files')
