# music/admin.py
from django.contrib import admin
from .models import SheetMusic, Mp3

admin.site.register(SheetMusic)
admin.site.register(Mp3)