from django.urls import reverse_lazy
from django.shortcuts import redirect, render
from django.core.mail import send_mail, mail_admins
from django.views.generic import TemplateView, CreateView
from django.contrib.auth.decorators import login_required

from bidzup import settings
from .forms import *
from utenti.mixins import *

class UserCreateView(CreateView):
    form_class = CreaCompratoreForm
    template_name = "utente_iscrizione.html"
    success_url = reverse_lazy("profilo")

class VenditoreCreateView(AnonymousRequiredMixin, UserCreateView):
    form_class = CreaVenditoreForm
    template_name = 'venditore_diventa.html'
    success_url = reverse_lazy("profilo")

    def form_valid(self, form):
        print("Form valido")
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        print("Utente salvato")

        gruppo, _ = Group.objects.get_or_create(name="Venditori")
        user.groups.add(gruppo)

        # Mail all'admin
        mail_admins(
            subject="Nuovo venditore in attesa di approvazione",
            message=(
                f"Un nuovo venditore si è registrato:\n\n"
                f"Username: {user.username}\n"
                f"Email: {user.email}\n\n"
                f"Accedi al pannello admin per approvarlo."
            )
        )
        print("Mail inviata all'admin")

        # Mail al venditore
        send_mail(
            subject="Registrazione inviata - Bidzup",
            message=(
                f"Ciao {user.username},\n\n"
                "Grazie per la tua richiesta di registrazione come venditore.\n"
                "Un amministratore la esaminerà al più presto.\n\n"
                "Riceverai una mail quando il tuo account sarà approvato.\n\n"
                "Grazie,\nIl team di Bidzup"
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=True
        )
        print("Mail inviata al venditore")
        return super().form_valid(form)

@login_required
def profilo_view(request):
    user = request.user

    if user.groups.filter(name='Venditori').exists():
        return redirect('profilo_venditore')

    elif user.groups.filter(name='Compratori').exists():
        return redirect('profilo_utente')
    else:
        return redirect('')

@login_required
def profilo_venditore(request):
    return render(request, "venditore_profilo.html")

@login_required
def profilo_utente(request):
    return render(request, "utente_profilo.html")

def has_group(user):
    return user.groups.filter(name="Venditori").exists()