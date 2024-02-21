from django.db import models
from django.contrib.auth.models import User
User._meta.get_field('email')._unique = True
User._meta.get_field('email').blank = False

import uuid

class Note(models.Model):
    id = models.UUIDField(default = uuid.uuid4, unique = True, primary_key = True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_notes')
    shared_with = models.ManyToManyField(User, related_name='shared_notes', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class NoteChange(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='changes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    changes_to_title = models.TextField(default = '')
    changes_to_content = models.TextField(default = '')

    def __str__(self):
        return f'{self.user.username} - {self.timestamp}'