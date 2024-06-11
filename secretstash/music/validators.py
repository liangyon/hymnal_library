from django.core.exceptions import ValidationError


def validate_pdf_extension(value):
    if value.file.content_type != 'application/pdf':
        raise ValidationError('Invalid file format. Only PDF files are allowed.')


def validate_audio_extension(value):
    if value.file.content_type not in ['audio/mpeg', 'audio/mp3', 'video/mp4']:
        raise ValidationError('Invalid file format. Only MP3, and MP4 files are allowed.')
