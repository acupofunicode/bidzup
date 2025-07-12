from django.contrib import admin
from django.urls import path, include
from .views import *
from core.initcmds import crea_gruppi_utenti

urlpatterns = [
    path('le-mie-aste/', AstaListView.as_view(), name='elenco_aste' ),
    path("le-mie-aste/nuova/", AstaCreateView.as_view(), name="crea_asta"),
    path('le-mie-aste/<int:pk>/', AstaDetailView.as_view(), name='asta_dettaglio'),
    path('le-mie-aste/<int:pk>/delete', AstaDeleteView.as_view(), name='asta_cancella'),
    path('le-mie-aste/<int:pk>/edit', AstaUpdateView.as_view(), name='asta_modifica'),
    path('le-mie-aste/pubblica/<int:pk>/', AstaUpdateView.pubblica_asta, name='pubblica_asta'),
    path('le-mie-aste/chiudi/<int:pk>/', AstaUpdateView.chiudi_asta, name='chiudi_asta'),
    path('asta/<int:pk>/offerta', OffertaCreateView.as_view(), name='fai_offerta'),
    path('ricerca/', AstaSearchView.as_view(), name='ricerca_aste'),

]