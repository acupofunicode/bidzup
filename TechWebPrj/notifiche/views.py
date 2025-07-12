from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import View, DetailView, ListView, DeleteView

from notifiche.models import *

# Create your views here.
class NotificaListView(ListView):
    model = Notifica
    context_object_name = 'notifica_list'
    template_name = 'notifiche/notifiche_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context_object_name = {'notifiche': Notifica.objects.filter(destinatario=self.request.user).order_by('-created_at')}
        return context_object_name

class NotificaDetailView(DetailView):
    model = Notifica
    context_object_name = 'notifica'
    template_name = 'notifiche/notifica_detail.html'

class NotificaSegnaComeLettaView(View):
    model = Notifica
    context_object_name = 'notifica'

    def post(self, request, pk, *args, **kwargs):
        notifica = Notifica.objects.filter(pk=pk, destinatario=self.request.user).first()
        notifica.messaggio_letto()
        return redirect('notifiche')

class NotificaCancellaMessaggioView(View):
    model = Notifica
    context_object_name = 'notifica'

    def post(self, request, pk, *args, **kwargs):
        notifica = Notifica.objects.filter(pk=pk, destinatario=self.request.user).first()
        notifica.cancella_messaggio()
        messages.success(self.request, "Asta eliminata")
        return redirect('notifiche')

