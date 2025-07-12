from django.urls import path

from aste.views import OffertaCreateView
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('', views.page_home, name='page_home'),
    path('chi-siamo/', views.page_about, name='chi-siamo'),
    path('aiuto/', views.page_help, name='aiuto'),
    path('contatti/', views.page_contact, name='contatti'),
    path('vendere/', views.page_sell, name='vendere'),
    path('accesso-negato/', views.accesso_negato, name='accesso_negato'),
    path('aste/', views.aste_vedi_tutte, name='aste_vedi_tutte'),
    path('categoria/<int:pk>/', views.page_categoria, name='categoria'),
    path('asta/<int:pk>', views.utente_asta, name='utente_asta'),
    path('compra/<int:pk>/', views.compra_subito, name='compra_subito'),
    path('aste-vinte/', views.aste_vinte, name='aste_vinte'),
    path('aste-in-corso/', views.aste_in_corso, name='aste_in_corso'),
    path('aste-terminate/', views.aste_terminate, name='aste_terminate'),
    path('aste-segui/<int:pk>', views.segui_asta, name='segui_asta'),
    path('aste-segui/<int:pk>/delete', views.segui_asta_stop, name='segui_asta_stop'),
    path('aste-terminate/<int:pk>', views.aste_terminate_dettaglio, name='aste_terminate_dettaglio'),
    path('acquistati/<int:pk>', views.utente_acquisto, name='utente_acquisto'),
]