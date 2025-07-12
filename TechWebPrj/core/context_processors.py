from aste.models import Categoria
from notifiche.models import Notifica

def categorie_context(request):
    return {
        'categorie': Categoria.objects.all()
    }

def notifiche_context(request):
    if request.user.is_authenticated:
        notifiche = Notifica.objects.filter(destinatario=request.user, is_read=False).order_by('-created_at')
        return {
            'non_lette': notifiche.count()
        }
    else:
        return {}