from aste.models import *
from notifiche.models import *
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

def crea_gruppi_utenti():
    venditori, created = Group.objects.get_or_create(name='Venditori')
    compratori = Group.objects.get_or_create(name='Compratori')
    asta_ct = ContentType.objects.get_for_model(Asta)

    perm_asta, created = Permission.objects.get_or_create(
        codename='can_do_asta',
        name='Creare aste',
        content_type=asta_ct
    )
    venditori.permissions.add(perm_asta)

def erase_db():
    print("Cancello il DB")
    Categoria.objects.all().delete()
    Asta.objects.all().delete()
    Offerta.objects.all().delete()
    Notifica.objects.all().delete()

def init_db():
    #print("Creo il DB")
    if len(Asta.objects.all()) != 0:
        return
    Categoria.objects.all().delete()
    categorie = ['Antiquariato', 'Modernariato', 'Auto e Moto', 'Giocattoli vintage', 'Gioielli', 'Arte', 'Moda']
    for i in categorie:
        c = Categoria()
        c.name = i
        c.save()