# music/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('upload/sheet_music/', views.upload_sheet_music, name='upload_sheet_music'),
    path('upload/mp3/', views.upload_mp3, name='upload_mp3'),
]
