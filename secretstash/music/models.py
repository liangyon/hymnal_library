# music/models.py
from django.db import models
from django.contrib.auth.models import User


class SheetMusic(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    file = models.FileField(upload_to='sheet_music/')

    def __str__(self):
        return self.title


