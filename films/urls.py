from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('film/<int:pk>/', views.film_detail, name='film_detail'),
    path('szukaj/', views.search, name='search'),
    path('film/<int:pk>/ulubione/', views.toggle_favorite, name='toggle_favorite'),
    path('film/<int:pk>/ocen/', views.add_rating, name='add_rating'),
    path('film/<int:pk>/komentarz/', views.add_comment, name='add_comment'),
    path('komentarz/<int:pk>/usun/', views.delete_comment, name='delete_comment'),
    path('ulubione/', views.favorites_list, name='favorites_list'),
    path('historia/', views.watch_history, name='watch_history'),
]
