# wedding/serializers.py

from rest_framework import serializers
from .models import StoryEntry

class StoryEntrySerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = StoryEntry
        fields = '__all__'

    def get_image(self, obj):
        return obj.image.url if obj.image else None