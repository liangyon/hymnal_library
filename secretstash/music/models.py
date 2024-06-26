# music/models.py
from django.db import models
from .validators import validate_pdf_extension, validate_audio_extension
from taggit.managers import TaggableManager


class SheetMusic(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(default='', null=True, blank=True)
    lyrics = models.TextField(default='', null=True, blank=True)
    lyricsAuthor = models.TextField(max_length=35, default='', null=True, blank=True)
    musicAuthor = models.TextField(max_length=35, default='', null=True, blank=True)
    tjchymn = models.BooleanField(default=False)
    pdf = models.FileField(upload_to='sheet_music', validators=[validate_pdf_extension], null=True, blank=True)
    playable = models.FileField(upload_to='mp3', validators=[validate_audio_extension], null=True, blank=True)
    tags = TaggableManager()

    def __str__(self):
        return self.title
