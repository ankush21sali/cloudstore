from django.urls import path
from . import views

app_name = 'files'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('videos/', views.videos, name='videos'),
    path('images/', views.images, name='images'),
    path('docs/', views.docs, name='docs'),
    path('audios/', views.audios, name='audios'),


    path('delete_file/<int:id>/', views.delete_file, name='delete_file'),
    path('folder/<slug:slug>/', views.folder_detail, name='folder_detail'),
    path("delete_folder/<int:folder_id>/", views.delete_folder, name="delete_folder"),
    path('favourites/', views.favourites, name='favourites'),
    path('favourite_item/<int:id>/', views.favourite_item, name='favourite_item'),
]
