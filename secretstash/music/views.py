# music/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import Http404, FileResponse
from .forms import SheetMusicForm
from .models import SheetMusic
import os


def index(request):
    try:
        items = SheetMusic.objects.all()
    except items.DoesNotExist:
        raise Http404("No musics exist")
    return render(request, 'music/index.html', {'items': items})


@login_required()
def download_music(request, file_id):
    sheet_music = get_object_or_404(SheetMusic, id=file_id)

    if sheet_music.pdf:
        file_path = sheet_music.pdf.path
        if os.path.exists(file_path):
            response = FileResponse(open(file_path, 'rb'))
            response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
            return response
        else:
            raise Http404("File not found")
    else:
        raise Http404("File not found")


@login_required()
def upload_sheet_music(request):
    if request.method == 'POST':
        form = SheetMusicForm(request.POST, request.FILES)
        if form.is_valid():
            sheet_music = form.save(commit=False)
            sheet_music.user = request.user
            sheet_music.save()
            return render(request, 'music/index.html', {'form': form})
    else:
        form = SheetMusicForm()
    return render(request, 'music/upload_sheet_music.html', {'form': form})


@login_required()
def music_page(request, sheetID):
    sheet = get_object_or_404(SheetMusic, id=sheetID)
    return render(request, 'music/music_page.html', {'sheet': sheet})


@login_required()
def music_list(request):
    try:
        items = SheetMusic.objects.all()
    except items.DoesNotExist:
        raise Http404("No musics exist")
    return render(request, 'music/music_list.html', {'items': items})


def login_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('index.html')
    else:
        return redirect('music/registration/login.html')
