#!/usr/bin/env python
"""
Batch compress and upload all static images to Cloudinary.
Organizes uploads by folder matching the local directory structure.

Usage:
    python scripts/upload_to_cloudinary.py
"""

import os
import sys
import json
from pathlib import Path
from io import BytesIO

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wedding_site.settings')
import django
django.setup()

from django.conf import settings
from PIL import Image
import cloudinary
import cloudinary.uploader

# Configure Cloudinary (reads credentials from .env via Django settings)
cloudinary.config(
    cloud_name=settings.CLOUDINARY_STORAGE['CLOUD_NAME'],
    api_key=settings.CLOUDINARY_STORAGE['API_KEY'],
    api_secret=settings.CLOUDINARY_STORAGE['API_SECRET'],
)

STATIC_ROOT = PROJECT_ROOT / 'wedding' / 'static'

# Upload mapping: (local_dir, cloudinary_folder, max_width, quality, resource_type)
UPLOAD_CONFIGS = [
    # Gallery photos — heavy compression
    ('images/gallery/denver-botanic-gardens', 'wedding-site/gallery/denver-botanic-gardens', 2000, 82, 'image'),
    ('images/gallery/telluride', 'wedding-site/gallery/telluride', 2000, 82, 'image'),
    # Background images
    ('images/backgrounds', 'wedding-site/backgrounds', 2000, 85, 'image'),
    # Itinerary illustrations (smaller PNGs, keep quality high)
    ('images/itinerary', 'wedding-site/itinerary', 1200, 90, 'image'),
    # Our Story images
    ('images/ourStory', 'wedding-site/our-story', 1600, 85, 'image'),
    # Header (logo, favicon — keep crisp)
    ('images/header', 'wedding-site/header', None, 95, 'image'),
    # Honeymoon fund
    ('honeymoon_fund', 'wedding-site/honeymoon-fund', 1600, 85, 'image'),
]

# Track all uploads for reference
upload_manifest = {}


def compress_image(filepath, max_width=None, quality=85):
    """Compress an image and return bytes. Returns (bytes, format)."""
    img = Image.open(filepath)

    # Convert RGBA to RGB for JPEG output (keep PNG for transparency)
    has_transparency = img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info)

    if max_width and img.width > max_width:
        ratio = max_width / img.width
        new_height = int(img.height * ratio)
        img = img.resize((max_width, new_height), Image.LANCZOS)

    buffer = BytesIO()

    if has_transparency:
        # Keep as PNG for images with transparency
        img.save(buffer, format='PNG', optimize=True)
        fmt = 'png'
    else:
        # Convert to RGB and save as JPEG
        if img.mode != 'RGB':
            img = img.convert('RGB')
        img.save(buffer, format='JPEG', quality=quality, optimize=True)
        fmt = 'jpg'

    buffer.seek(0)
    original_size = os.path.getsize(filepath)
    compressed_size = buffer.getbuffer().nbytes

    return buffer, fmt, original_size, compressed_size


def upload_file(buffer, folder, public_id, resource_type='image'):
    """Upload a file buffer to Cloudinary."""
    result = cloudinary.uploader.upload(
        buffer,
        folder=folder,
        public_id=public_id,
        overwrite=True,
        resource_type=resource_type,
    )
    return result


def process_directory(local_dir, cloud_folder, max_width, quality, resource_type):
    """Compress and upload all images in a directory."""
    full_path = STATIC_ROOT / local_dir

    if not full_path.exists():
        print(f"  SKIP: {local_dir} does not exist")
        return

    # Get image files (skip directories and hidden files)
    extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
    files = sorted([
        f for f in full_path.iterdir()
        if f.is_file() and f.suffix.lower() in extensions and not f.name.startswith('.')
    ])

    if not files:
        print(f"  SKIP: No image files in {local_dir}")
        return

    total_original = 0
    total_compressed = 0

    for filepath in files:
        # Sanitize public_id: replace & with _and_, remove other invalid chars
        public_id = filepath.stem.replace('&', '_and_')

        try:
            buffer, fmt, orig_size, comp_size = compress_image(filepath, max_width, quality)
            total_original += orig_size
            total_compressed += comp_size

            result = upload_file(buffer, cloud_folder, public_id)

            orig_mb = orig_size / (1024 * 1024)
            comp_kb = comp_size / 1024
            print(f"  {filepath.name}: {orig_mb:.1f} MB -> {comp_kb:.0f} KB | {result['secure_url']}")

            upload_manifest[f"{local_dir}/{filepath.name}"] = {
                'public_id': result['public_id'],
                'url': result['secure_url'],
                'format': result['format'],
                'width': result['width'],
                'height': result['height'],
                'bytes': result['bytes'],
            }

        except Exception as e:
            print(f"  ERROR {filepath.name}: {e}")

    orig_total_mb = total_original / (1024 * 1024)
    comp_total_mb = total_compressed / (1024 * 1024)
    reduction = (1 - total_compressed / total_original) * 100 if total_original > 0 else 0
    print(f"  Subtotal: {orig_total_mb:.1f} MB -> {comp_total_mb:.1f} MB ({reduction:.0f}% reduction)")


def main():
    print("=" * 60)
    print("Cloudinary Batch Upload")
    print("=" * 60)

    for local_dir, cloud_folder, max_width, quality, resource_type in UPLOAD_CONFIGS:
        print(f"\n[{cloud_folder}]")
        process_directory(local_dir, cloud_folder, max_width, quality, resource_type)

    # Save manifest
    manifest_path = PROJECT_ROOT / 'scripts' / 'cloudinary_manifest.json'
    with open(manifest_path, 'w') as f:
        json.dump(upload_manifest, f, indent=2)

    print(f"\n{'=' * 60}")
    print(f"Upload complete! {len(upload_manifest)} files uploaded.")
    print(f"Manifest saved to: {manifest_path}")
    print("=" * 60)


if __name__ == '__main__':
    main()
