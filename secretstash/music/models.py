# music/models.py
from django.db import models
from django.contrib.auth.models import User


class SheetMusic(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='sheet_music/')

    def __str__(self):
        return self.title


class Mp3(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='mp3s/')

    def __str__(self):
        return self.title
