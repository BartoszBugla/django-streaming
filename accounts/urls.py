from django.urls import path
from . import views

urlpatterns = [
    path('rejestracja/', views.register_view, name='register'),
    path('logowanie/', views.login_view, name='login'),
    path('wyloguj/', views.logout_view, name='logout'),
    path('profil/', views.profile_view, name='profile'),
]
