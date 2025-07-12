import datetime

from django.contrib.auth.models import User

from aste.models import Categoria, Asta, Offerta, AstaSeguita
from notifiche.utils import *
from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from utenti.mixins import *
def page_home(request):
    categorie = Categoria.objects.all()
    aste = Asta.objects.filter(is_active=True).order_by('-created_at')[:3]
    aste_terminate = Asta.objects.filter(is_active=False).order_by('-created_at')[:4]
    return render(request, 'home.html', {'categorie': categorie, 'aste': aste, 'aste_terminate': aste_terminate})
def page_about(request):
    return render(request, template_name="about.html")
def page_help(request):
    return render(request, template_name="help.html")
def page_contact(request):
    return render(request, template_name="contatti.html")
def page_sell(request):
    return render(request, template_name="vendere.html")
def accesso_negato(request):
    return render(request, 'accesso_negato.html')
def aste_vedi_tutte(request):
    aste = Asta.objects.filter(is_active=True).order_by('-created_at')
    return render(request, 'aste/utente_asta_list.html',{'aste': aste})
def page_categoria(request, pk):
    categoria = Categoria.objects.get(pk=pk)
    aste = Asta.objects.filter(is_active=True, categoria=pk).order_by('-created_at')
    return render(request, 'utente_categorie_list.html', {'aste': aste, 'categoria':categoria})
@login_required
def aste_in_corso(request):
    aste = Asta.objects.filter(offerte__offerente=request.user, is_active=True).distinct()
    return render(request, 'aste/utente_aste_in_corso.html', {'aste': aste})
@login_required
def aste_vinte(request):
    aste = Asta.objects.filter(winner=request.user)
    return render(request, 'aste/utente_aste_vinte.html', {'aste': aste})
@login_required
def aste_terminate(request):
    aste = Asta.objects.filter(offerte__offerente=request.user, is_active=False).exclude(winner=request.user).distinct()
    return render(request, 'aste/utente_aste_terminate.html', {'aste': aste})
@login_required
def aste_terminate_dettaglio(request, pk):
    asta = Asta.objects.filter(offerte__offerente=request.user, is_active=False, pk=pk).exclude(winner=request.user).distinct()
    offerte = Offerta.objects.filter(offerente=request.user, asta=pk)
    return render(request, 'aste/utente_aste_terminate_dettaglio.html', {'asta': asta, 'offerte': offerte})
@solo_compratori
def compra_subito(request, pk):
    asta = Asta.objects.get(pk=pk)
    asta.winner = request.user
    asta.final_price = asta.buynow_price
    asta.data_fine = datetime.date.today()
    asta.close()

    notifica_compra_subito(asta, asta.winner)
    messages.error(request, "Complimenti! Acquisto confermato.")
    return render(request, 'aste/utente_aste_vinte.html', {'asta': asta})
def utente_asta(request, pk):
    asta = Asta.objects.get(pk=pk)
    offerta_maggiore = ''

    if asta.is_active:
        if not request.user.is_anonymous:
            segue = asta.followers.filter(user=request.user).exists()

            if Offerta.objects.filter(asta=asta, offerente=request.user).exists() :
                # offerta maggiore e' differenza tra quella piu' alta dell'utente e quella piu' alta in generale
                offerta_utente_top = Offerta.objects.filter(offerente=request.user, asta=asta).order_by('-importo').first()
                offerta_top = Offerta.objects.filter(asta=asta).order_by('-importo').first()
                offerta_maggiore = offerta_top.importo - offerta_utente_top.importo
            return render(request, 'aste/utente_asta.html',{'asta': asta, 'offerta_maggiore':offerta_maggiore, 'segue': segue})
        else:
            return render(request, 'aste/utente_asta.html', {'asta': asta})
    else:
        messages.error(request, "Accesso negato per asta conclusa.")
        return render(request, 'accesso_negato.html')
@login_required
def utente_acquisto(request, pk):
    acquistato = Asta.objects.get(pk=pk)
    if acquistato.winner == request.user:
        return render(request, 'aste/utente_acquisto.html',{'acquisto': acquistato})
    else:
        messages.error(request, "Accesso negato per asta in corso o conclusa da altro acquirente.")
        return render(request, 'accesso_negato.html')

@solo_compratori
def segui_asta(request, pk):
    asta = Asta.objects.get(pk=pk)
    AstaSeguita.objects.create(asta=asta, user=request.user)
    return redirect('utente_asta', pk=asta.id)

@solo_compratori
def segui_asta_stop(request, pk):
    astaseguita = AstaSeguita.objects.filter(asta=Asta.objects.get(pk=pk), user=request.user)
    astaseguita.delete()
    return redirect('utente_asta', pk=pk)