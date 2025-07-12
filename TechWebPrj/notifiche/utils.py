import datetime

from aste.models import Asta, AstaSeguita
from .models import Notifica

def notifica_aste_chi_segue(asta, user, messaggio):
    followers = AstaSeguita.objects.filter(asta=asta).exclude(user=user)
    for follower in followers:
        Notifica.objects.create(
            asta=asta,
            destinatario=follower.user.username,
            titolo="Aggiornamento su un\'asta che stai seguendo",
            messaggio=messaggio,
            is_read=False,
            created_at=datetime.datetime.now(),
        )

def notifica_offerta_superata( asta, offerta ):
    from aste.models import Offerta
    offerte = Offerta.objects.filter(asta=asta).exclude(offerente=offerta.offerente).order_by('offerente')
    elenco_offerenti = []
    for offerta in offerte:
        elenco_offerenti.append(offerta.offerente)
    offerenti = list(set(elenco_offerenti))
    if offerenti:
        for offerente in offerenti:
            Notifica.objects.create(
                destinatario=offerente,
                titolo="La tua offerta e\' stata superata",
                asta=asta,
                messaggio=f"Ci spiace informarti che la tua offerta per \"{asta.titolo}\" e\' stata superata.",
                is_read=False,
                created_at=datetime.datetime.now(),
            )

def notifica_offerta( asta, offerta ):
    messaggio=f"{offerta.offerente.username} ha fatto un\' di {offerta.importo} € per l'asta \"{asta.titolo}\"."
    Notifica.objects.create(
        destinatario=asta.owner,
        titolo="Nuova offerta ricevuta",
        asta=asta,
        messaggio=messaggio,
        is_read=False,
        created_at=datetime.datetime.now(),
    )
    notifica_aste_chi_segue(asta, offerta.offerente, messaggio)
    Notifica.objects.create(
        destinatario=offerta.offerente,
        titolo="Nuova offerta inviata",
        asta=asta,
        messaggio=f"Hai appena fatto una nuova offerta di un\' di {offerta.importo} € per l'asta \"{asta.titolo}\".",
        is_read=False,
        created_at=datetime.datetime.now(),
    )

    notifica_offerta_superata(asta, offerta)

def notifica_compra_subito( asta, compratore ):
    messaggio = f"{compratore.username} ha acquistato subito  \"{asta.titolo}\".",
    Notifica.objects.create(
        destinatario=asta.owner,
        titolo="Oggetto Venduto",
        asta=asta,
        messaggio=messaggio,
        is_read=False,
        created_at=datetime.datetime.now(),
    )
    notifica_aste_chi_segue(asta, compratore, messaggio)

    Notifica.objects.create(
        destinatario=compratore,
        asta=asta,
        titolo="Acquisto completato",
        messaggio=f"Complimenti, hai appena acquistato \"{asta.titolo}\".",
        is_read=False,
        created_at=datetime.datetime.now(),
    )

    from aste.models import Offerta
    offerte = Offerta.objects.filter(asta=asta).exclude(offerente=asta.winner).order_by('offerente')
    elenco_offerenti = []
    for offerta in offerte:
        elenco_offerenti.append(offerta.offerente)
    offerenti = list(set(elenco_offerenti))

    if offerenti:
        for offerente in offerenti:
            Notifica.objects.create(
                destinatario=offerente,
                titolo="Asta terminata ",
                asta=asta,
                messaggio=f"Siamo spiacenti di informarti che qualcuno ha comprato \"{asta.titolo}\".",
                is_read=False,
                created_at=datetime.datetime.now(),
            )

def notifica_asta_scaduta( asta ):
    Notifica.objects.create(
        destinatario=asta.owner,
        titolo="Asta scaduta",
        asta=asta,
        messaggio=f"Asta: \"{asta.titolo}\". scaduta",
        is_read=False,
        created_at=datetime.datetime.now(),
    )

def notifica_asta_vinta( asta ):
    compratore = asta.winner
    messaggio = f"{compratore.username} ha vinto l'asta  \"{asta.titolo}\".",
    Notifica.objects.create(
        destinatario=asta.owner,
        asta=asta,
        titolo="Oggetto Venduto",
        messaggio=messaggio,
        is_read=False,
        created_at=datetime.datetime.now(),
    )
    notifica_aste_chi_segue(asta, compratore, messaggio)
    Notifica.objects.create(
        asta=asta,
        destinatario=compratore,
        titolo="Hai vinto!",
        messaggio=f"Complimenti, ti sei aggiudicato \"{asta.titolo}\".",
        is_read=False,
        created_at=datetime.datetime.now(),
    )