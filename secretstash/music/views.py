# music/views.py
from django.shortcuts import render, redirect
from .forms import SheetMusicForm
from .models import SheetMusic


def index(request):
    items = SheetMusic.objects.all()
    return render(request, 'music/index.html', {'items': items})


def upload_sheet_music(request):
    if request.method == 'POST':
        form = SheetMusicForm(request.POST, request.FILES)
        if form.is_valid():
            sheet_music = form.save(commit=False)
            sheet_music.user = request.user
            sheet_music.save()
            return render(request, 'music/upload_sheet_music.html', {'form': form})
    else:
        form = SheetMusicForm()
    return render(request, 'music/upload_sheet_music.html', {'form': form})


