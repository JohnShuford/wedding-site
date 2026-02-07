from django.db import models
from ckeditor.fields import RichTextField

class StoryEntry(models.Model):
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=225, blank=True, null=True)
    date = models.DateField()
    description = RichTextField()
    image = models.ImageField(upload_to='our_story_photos/')

    class Meta:
        ordering = ['date']
        verbose_name_plural = "Story Entries"

    def __str__(self):
        return f"{self.date} - {self.title}"