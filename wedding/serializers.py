# wedding/serializers.py

from rest_framework import serializers
from .models import StoryEntry

class StoryEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = StoryEntry
        fields = '__all__'