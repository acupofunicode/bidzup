from django.urls import path
from notifiche.views import NotificaListView, NotificaSegnaComeLettaView, NotificaDetailView, NotificaCancellaMessaggioView
urlpatterns = [
    path('notifiche/', NotificaListView.as_view(), name='notifiche'),
    path('notifica/<int:pk>', NotificaDetailView.as_view(), name='leggi_notifica'),
    path('notifica/<int:pk>/read', NotificaSegnaComeLettaView.as_view(), name='segna_come_letto'),
    path('notifica/<int:pk>/delete', NotificaCancellaMessaggioView.as_view(), name='cancella_notifica')
]