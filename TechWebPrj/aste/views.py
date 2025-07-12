from django.utils import timezone
from django.views.generic import CreateView, DetailView, ListView, DeleteView, UpdateView, FormView
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect
from .models import *
from .forms import AstaForm, AllegatoFormSet, AllegatoForm, OffertaForm
from utenti.mixins import GroupRequiredMixin, GroupRequiredCompratoreMixin
from notifiche.utils import *
class AstaCreateView(GroupRequiredMixin, CreateView):
    model = Asta
    form_class = AstaForm
    template_name = 'aste/venditore_asta_nuova.html'
    success_url = reverse_lazy('elenco_aste')
    group_required = 'Venditori'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = AllegatoFormSet(self.request.POST, self.request.FILES,
                                                 queryset=Allegato.objects.none())
        else:
            context['formset'] = AllegatoFormSet(queryset=Allegato.objects.none())
        return context

    def form_valid(self, form):
        user = self.request.user
        if not user.groups.filter(name='Venditori').exists() or not user.is_active:
            return redirect('non_autorizzato')  # o mostra un messaggio
        context = self.get_context_data()
        formset = context['formset']
        form.instance.owner = self.request.user
        if formset.is_valid():
            self.object = form.save()
            for image_form in formset.cleaned_data:
                if image_form and image_form.get('immagine'):
                    Allegato.objects.create(asta=self.object, immagine=image_form['immagine'])
            messages.success(self.request, "Asta creata con successo!")
            return super().form_valid(form)
        else:
            return self.form_invalid(form)

class AstaDetailView(GroupRequiredMixin, DetailView):
    model = Asta
    template_name = 'aste/venditore_asta.html'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.owner != request.user:
            return redirect('accesso_negato')
        offerte = Offerta.objects.filter(asta=self.object)
        self.offerte = offerte
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context_object_name = {'offerte': Offerta.objects.filter(asta=self.object).order_by('-data'), 'asta': self.object}
        return context_object_name

class AstaListView(GroupRequiredMixin, ListView):
    model = Asta
    template_name = 'aste/venditore_asta_list.html'

    def get_context_data(self, **kwargs):
        context_object_name = {'aste': Asta.objects.filter(owner=self.request.user).order_by('-created_at')}
        return context_object_name

class AstaDeleteView(GroupRequiredMixin, DeleteView):
    model = Asta
    template_name = 'aste/venditore_asta_cancella.html'
    success_url = "/le-mie-aste"

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.owner != request.user:
            return redirect('accesso_negato')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        messages.success(self.request, "Asta eliminata")
        return super().form_valid(form)

class AstaUpdateView(GroupRequiredMixin, UpdateView):
    model = Asta
    form_class = AstaForm
    success_url = "/le-mie-aste"
    template_name = 'aste/venditore_asta_modifica.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = AllegatoFormSet(
                self.request.POST, self.request.FILES,
                queryset=Allegato.objects.filter(asta=self.object)
            )
        else:
            context['formset'] = AllegatoFormSet(
                queryset=Allegato.objects.filter(asta=self.object)
            )
        return context

    def pubblica_asta(self, pk):
        asta = Asta.objects.get(pk=pk)
        asta.is_active = True
        asta.save()
        messages.success(self, "Asta pubblicata")
        return redirect('asta_dettaglio', pk=asta.pk)

    def chiudi_asta(self, pk):
        asta = Asta.objects.get(pk=pk)
        if asta.current_highest_bid.importo >= asta.reserve_price:
            asta.winner = asta.current_highest_bid.offerente
            asta.final_price = asta.current_highest_bid.importo
            notifica_asta_vinta(asta)

        asta.close()

        messages.success(self, "Asta Chiusa")
        return redirect('asta_dettaglio', pk=asta.pk)

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid():
            asta = form.save()
            for allegato_form in formset:
                if allegato_form.cleaned_data:
                    allegato = allegato_form.save(commit=False)
                    allegato.asta = asta
                    allegato.save()
                    if allegato_form.cleaned_data.get('DELETE'):
                        allegato.delete()
            messages.success(self.request, "Asta modificata")
            return redirect('asta_dettaglio', pk=asta.pk)
        else:
            return self.form_invalid(form)

class AstaSearchView(ListView):
    model = Asta
    template_name = 'ricerca_aste.html'
    context_object_name = 'aste'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorie'] = Categoria.objects.all()
        return context

    def get_queryset(self):
        query = self.request.GET.get('q')
        categoria_id = self.request.GET.get('categoria')

        # Partiamo da queryset vuoto o da una combinazione OR
        if query:
            qs_titolo = Asta.objects.filter(titolo__icontains=query, is_active=True)
            qs_descrizione = Asta.objects.filter(descrizione__icontains=query, is_active=True)
            queryset = (qs_titolo | qs_descrizione)
            print(queryset)
        else:
            queryset = Asta.objects.filter(is_active=True)

        if categoria_id:
            queryset = queryset.filter(categoria_id=categoria_id)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categoria = Categoria.objects.get(id=self.request.GET.get('categoria')).name
        context['titolo_pagina'] = categoria
        return context
class OffertaCreateView( GroupRequiredCompratoreMixin, FormView ):
    form_class = OffertaForm
    template_name = 'aste/utente_offerta.html'

    def dispatch(self, request, *args, **kwargs):
        asta = Asta.objects.get(pk=kwargs['pk'])
        if asta is not None:
            self.asta = asta
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('accesso_negato')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['asta'] = self.asta  # passa l’oggetto al form
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['asta'] = self.asta
        offerte_fatte = Offerta.objects.filter(asta=self.asta, offerente=self.request.user)
        context['offerte_fatte'] = offerte_fatte
        return context

    def form_valid(self, form):
        importo = form.cleaned_data['importo']
        offerta_corrente = self.asta.offerte.order_by('-importo').first()

        if offerta_corrente and importo <= offerta_corrente.importo:
            form.add_error('importo', 'Offerta troppo bassa')
            return self.form_invalid(form)

        offerta = form.save(commit=False)
        offerta.asta = self.asta
        offerta.data = timezone.now()
        offerta.offerente = self.request.user
        offerta.save()

        notifica_offerta( self.asta, offerta)

        messages.success(self.request, "Complimenti, offerta effettuata!")
        return redirect('utente_asta',pk=offerta.asta.pk)