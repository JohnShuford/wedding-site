from django.db import models
class StoryEntry(models.Model):
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=225, blank=True, null=True)
    date = models.DateField()
    description = models.TextField()
    image = models.ImageField(upload_to='our_story_photos/')
    
    def __str__(self):
        return f"{self.date} - {self.title}"