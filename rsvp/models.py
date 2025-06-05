from django.db import models
import uuid

class Guest(models.Model):
    group_id = models.UUIDField(default=uuid.uuid4, editable=True, db_index=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    dietary_restrictions = models.TextField(blank=True)
    message_for_couple = models.TextField(blank=True)
    attending = models.BooleanField(null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
