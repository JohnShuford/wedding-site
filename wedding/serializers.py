# wedding/serializers.py

from rest_framework import serializers
from django.conf import settings
from .models import StoryEntry

CLOUDINARY_BASE = f"https://res.cloudinary.com/{settings.CLOUDINARY_STORAGE['CLOUD_NAME']}/image/upload"

class StoryEntrySerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = StoryEntry
        fields = '__all__'

    def get_image(self, obj):
        if not obj.image:
            return None
        return f"{CLOUDINARY_BASE}/c_limit,w_1200,q_auto,f_auto/{obj.image}"