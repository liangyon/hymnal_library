# music/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('upload/sheet_music/', views.upload_sheet_music, name='upload_sheet_music'),
    path('upload/multiple_sheet_music/', views.FileFieldFormView.as_view(), name='upload_multiple_sheet_music'),
    path('sheets/<int:sheetID>/', views.music_page, name='music_page'),
    path('accounts/login/',
         auth_views.LoginView.as_view(template_name='music/registration/login.html'),
         name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(template_name='music/registration/logout.html'),
         name='logout'),
    path('download/<int:sheetID>/', views.download_music, name='download_pdf'),
    path('display/<int:sheetID>/', views.display_pdf, name='display_pdf'),
    path('music_list/', views.music_list, name='music_list'),
    path('', views.index, name='index'),

]
