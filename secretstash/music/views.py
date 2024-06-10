# music/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import Http404
from .forms import SheetMusicForm
from .models import SheetMusic


def index(request):
    try:
        items = SheetMusic.objects.all()
    except items.DoesNotExist:
        raise Http404("Question doesnot exist")
    return render(request, 'music/index.html', {'items': items})


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
def music_page(request):
    return render(request, 'music/music_page.html')


def login_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('index.html')
    else:
        return redirect('music/registration/login.html')
