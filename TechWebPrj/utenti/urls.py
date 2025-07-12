from django.urls import path
from utenti.views import *
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('registrati/', UserCreateView.as_view(), name="registrati"),
    path('diventa-venditore/', VenditoreCreateView.as_view(), name="diventa-venditore"),
    path('login/', auth_views.LoginView.as_view(), name="login"),
    path('logout/', auth_views.LogoutView.as_view(), name="logout"),
    path('profilo/', profilo_view, name='profilo'),
    path("profilo/venditore/", profilo_venditore, name="profilo_venditore"),
    path("profilo/utente/", profilo_utente, name="profilo_utente")
]