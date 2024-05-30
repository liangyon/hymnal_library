# music/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('upload/sheet_music/', views.upload_sheet_music, name='upload_sheet_music'),
    path('', views.index, name='index'),

]
