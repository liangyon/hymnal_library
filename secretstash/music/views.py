# music/views.py
from django.shortcuts import render, redirect
from .forms import SheetMusicForm, Mp3Form

def upload_sheet_music(request):
    if request.method == 'POST':
        form = SheetMusicForm(request.POST, request.FILES)
        if form.is_valid():
            sheet_music = form.save(commit=False)
            sheet_music.user = request.user
            sheet_music.save()
            return redirect('sheet_music_list')
    else:
        form = SheetMusicForm()
    return render(request, 'music/upload_sheet_music.html', {'form': form})

def upload_mp3(request):
    if request.method == 'POST':
        form = Mp3Form(request.POST, request.FILES)
        if form.is_valid():
            mp3 = form.save(commit=False)
            mp3.user = request.user
            mp3.save()
            return redirect('mp3_list')
    else:
        form = Mp3Form()
    return render(request, 'music/upload_mp3.html', {'form': form})
