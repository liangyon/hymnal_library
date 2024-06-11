# music/forms.py
from django import forms
from .models import SheetMusic


class SheetMusicForm(forms.ModelForm):
    class Meta:
        model = SheetMusic
        fields = ['title', 'description', 'lyrics', 'lyricsAuthor', 'musicAuthor', 'tjchymn', 'pdf', 'playable']
