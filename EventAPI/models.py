from django.db import models
from django.contrib.auth.models import User

class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=1024)
    location = models.TextField(max_length=255)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='event_organizer')
    start_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    participants = models.ManyToManyField(User, related_name='event_partisipants')
