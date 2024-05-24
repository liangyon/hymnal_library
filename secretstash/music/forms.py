# music/forms.py
from django import forms
from .models import SheetMusic, Mp3

class SheetMusicForm(forms.ModelForm):
    class Meta:
        model = SheetMusic
        fields = ['title', 'description', 'file']

class Mp3Form(forms.ModelForm):
    class Meta:
        model = Mp3
        fields = ['title', 'description', 'file']