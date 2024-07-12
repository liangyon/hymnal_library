# music/forms.py
from django import forms
from .models import SheetMusic


class SheetMusicForm(forms.ModelForm):
    class Meta:
        model = SheetMusic
        fields = ['title', 'pdf']


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]
        return result

    def validate_file_type(self, file):
        # Validate file type here
        if not file.name.endswith('.pdf'):
            raise forms.ValidationError('Only PDF files are allowed.')


class FileFieldForm(forms.Form):
    file_field = MultipleFileField()



