from django.db import models
from django.contrib.auth.models import User
from aste.models import Asta

class Notifica(models.Model):
    destinatario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifica')
    titolo = models.CharField(max_length=255, default='Nuovo messaggio')
    messaggio = models.TextField(default='')
    asta = models.ForeignKey(Asta, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"To {self.destinatario.username}: {self.titolo[:50]}"

    def messaggio_letto(self):
        self.is_read = True
        self.save()

    def cancella_messaggio(self):
        self.delete()

    class Meta:
        verbose_name_plural = 'Notifiche'