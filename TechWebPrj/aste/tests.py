import datetime
from django.utils import timezone
from django.test import TestCase, Client
from django.contrib.auth.models import User, Group
from django.urls import reverse
from aste.models import Asta, Offerta, Categoria

# Create your tests here.
class TestOfferta(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="vendo_ora", password="dada123!")
        self.asta = Asta.objects.create(
            titolo="Bicicletta",
            descrizione="Bella bici da corsa",
            data_inizio=timezone.now(),
            data_fine=datetime.date.today()+datetime.timedelta(days=12),
            categoria=Categoria.objects.filter(name='Antiquariato').first(),
            reserve_price=99,
            buynow_price=200,
            owner=self.user
        )

    def test_offerta_valida(self):
        offerta = Offerta.objects.create(
            offerente=self.user,
            data=timezone.now(),
            asta=self.asta,
            importo=600
        )
        self.assertEqual(offerta.importo, 600)
        self.assertEqual(offerta.asta, self.asta)

    def test_offerta_maggiore(self):
        offerta1 = Offerta.objects.create(
            offerente=self.user,
            data=timezone.now(),
            asta=self.asta,
            importo=100
        )
        offerta2 = Offerta.objects.create(
            offerente=self.user,
            data=timezone.now(),
            asta=self.asta,
            importo=101
        )
        self.assertEqual(self.asta.current_highest_bid.importo, 101)

    def test_get_min_increment(self):
        self.assertEqual(Offerta.get_min_increment(self.asta.reserve_price), 5)

class TestFaiOffertaView(TestCase):
    def setUp(self):
        self.client = Client()
        self.venditori, created = Group.objects.get_or_create(name='Venditori')
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.user.groups.add(self.venditori)
        self.user.save()
        self.client.login(username='testuser', password='pass123')

    def test_crea_asta(self):
        self.asta = Asta.objects.create(
            titolo="Abito Chanel anno 60",
            descrizione="Uno dei primi abiti realizzati in tartan",
            data_inizio=timezone.now(),
            data_fine=datetime.date.today()+datetime.timedelta(days=12),
            categoria=Categoria.objects.filter(name='Moda').first(),
            reserve_price=700,
            buynow_price=1800,
            owner=self.user,
        )
        self.assertEqual(Asta.objects.count(), 1)

    def test_offerta_creata_con_post(self):
        self.asta = Asta.objects.create(
            titolo="Abito Chanel anno 60",
            descrizione="Uno dei primi abiti realizzati in tartan",
            data_inizio=timezone.now(),
            data_fine=datetime.date.today() + datetime.timedelta(days=12),
            categoria=Categoria.objects.filter(name='Moda').first(),
            reserve_price=700,
            buynow_price=1800,
            owner=self.user,
        )

        self.user = User.objects.create_user(username="customer", password="testpass")
        self.compratori, created = Group.objects.get_or_create(name='Compratori')
        self.user.groups.add(self.compratori)
        self.assertTrue(self.user.groups.filter(name='Compratori').exists())
        res = self.client.login(username="customer", password="testpass")
        self.assertEqual(res, True)

        response = self.client.post(reverse("fai_offerta", args=[self.asta.pk]), {
            "importo": 150
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Offerta.objects.count(), 1)

        offerta = Offerta.objects.first()
        self.assertEqual(offerta.importo, 150)
        self.assertEqual(offerta.asta, self.asta)
        self.assertEqual(offerta.offerente, self.user)