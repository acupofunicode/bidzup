import os
from datetime import date

from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import User

class Categoria(models.Model):
    name = models.CharField(max_length=100)
    class Meta:
        verbose_name_plural = 'Categorie'

    def __str__(self):
        return self.name

class Asta(models.Model):
    titolo = models.CharField(max_length=100)
    descrizione = models.TextField()
    data_inizio = models.DateTimeField('data inizio')
    data_fine = models.DateField()
    reserve_price = models.FloatField()
    buynow_price = models.FloatField()
    final_price = models.FloatField( null=True, blank=True)
    categoria = models.ForeignKey('Categoria', on_delete=models.SET(999))
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='aste')
    winner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True  )
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)

    @property
    def is_scaduta(self):
        return date.today() >= self.data_fine

    @property
    def current_highest_bid(self):
        if self.offerte.exists() :
            return self.offerte.order_by('-importo').first()
        else:
            return 0

    def close(self):
        self.is_active = False
        self.save()

    def __str__(self):
        out = "Asta " + self.titolo + " inizia il " + str(self.data_inizio) + " e si conclude il " + str(self.data_fine)
        return out

    class Meta:
        verbose_name_plural = 'Aste'

class Allegato(models.Model):
    def upload_to_per_asta(instance, filename):
        asta_id = instance.asta.id if instance.asta else 'temp'
        username_venditore = instance.asta.owner.username
        return os.path.join(f"galleria/{username_venditore}_{asta_id}", filename)

    asta = models.ForeignKey(Asta, related_name='immagini', on_delete=models.CASCADE)
    immagine = models.ImageField(upload_to=upload_to_per_asta)

class AstaSeguita(models.Model):
    asta = models.ForeignKey(Asta, on_delete=models.CASCADE, related_name='followers')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='aste_seguite')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'asta')

    def __str__(self):
        return f"{self.utente.username} segue {self.asta.titolo}"

class Offerta(models.Model):
    asta = models.ForeignKey(Asta, related_name='offerte', on_delete=models.CASCADE)
    offerente = models.ForeignKey(User, on_delete=models.CASCADE)
    importo = models.FloatField(default=0)
    data = models.DateTimeField()

    class Meta:
        verbose_name_plural = 'Offerte'
        ordering = ['-data']

    def __str__(self):
        return f"{self.offerente} - {self.importo} €"

    def get_min_increment(base_price):
        if base_price < 100:
            return 5
        elif base_price < 1000:
            return 50
        else:
            return 100