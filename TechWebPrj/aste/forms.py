from urllib import request

from django import forms
from .models import Asta, Allegato, Offerta
from django.contrib.auth import login
from django.forms import formset_factory, modelformset_factory

class AstaForm(forms.ModelForm):
    class Meta:
        exclude = ['owner', 'created_at', 'winner', 'final_price']

    data_inizio = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Inizio asta'
    )
    data_fine = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Fine asta'
    )
    reserve_price = forms.IntegerField(
        label='Prezzo di riserva. Si tratta del prezzo minimo per vendere l\'oggetto',
    )
    buynow_price = forms.IntegerField(
        label='Prezzo per acquisto immediato (Compralo subito)',
    )

    class Meta:
        model = Asta
        exclude = ['owner', 'is_active', 'created_at', 'winner', 'final_price']
        widgets = {
            'descrizione': forms.Textarea(attrs={
                'rows': 5,
                'class': 'form-control'
            }),
        }

class AllegatoForm(forms.ModelForm):
    model = Allegato
    fields = ['immagine']

AllegatoFormSet = modelformset_factory(
    form=AllegatoForm,
    extra=6,
    model=Allegato,
    fields=('immagine',)
)

class OffertaForm(forms.ModelForm):
    importo = forms.IntegerField(
        label='Importo',
    )
    class Meta:
        model = Offerta
        fields = ['importo' ]
        widgets = {
            'importo': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Inserisci la tua offerta'})
        }

    def __init__(self, *args, **kwargs):
        self.asta = kwargs.pop('asta', None)
        super().__init__(*args, **kwargs)

    def clean_importo(self):
        offerta_massima = 0
        importo = self.cleaned_data['importo']
        minimo_incremento = Offerta.get_min_increment(self.asta.reserve_price)
        if self.asta.offerte.count() > 0:
            offerta_massima = self.asta.current_highest_bid.importo
        if importo < minimo_incremento+offerta_massima:
            raise forms.ValidationError(
                f"Rilancio minimo pari a: {minimo_incremento:.2f} €"
            )
        return importo