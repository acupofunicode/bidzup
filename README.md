# Bidzup 

Bidzup è una piattaforma web di aste online in cui i venditori possono creare aste e gli acquirenti possono fare offerte o comprare subito gli oggetti messi all'asta. 
Un sistema di notifiche permette di tenere aggiornati venditori e compratori.

## Funzionalità principali

- Registrazione e login per compratori e venditori
- Creazione e modifica delle aste (solo venditori approvati)
- Caricamento multiplo di immagini per ogni asta
- Sistema di offerte
- Acquisto immediato con "Compralo Subito"
- Notifiche tra utenti

## Tecnologie usate

- Django
- SQLite 
- Bootstrap 4
- Crispy Forms



## Installazione locale

- Clona il progetto:   
   ```bash
   git clone https://github.com/tuo-username/bidzup.git
   cd bidzup

- Crea e attiva un ambiente virtuale
    ```bash
    pipenv shell 

- Applica le migrazioni
    ```bash
    python manage.py migrate    

- Crea un utente superuser (admin)
    ```bash
    python manage.py createsuperuser

- Avviare il server
    ```bash
    python manage.py runserver


## License
Released under [MIT License](LICENSE.txt).
## Screenshots
###### Login


###### Vista aste per venditore
<img width="1162" height="560" alt="Schermata 2025-07-11 alle 23 23 13" src="https://github.com/user-attachments/assets/f52259ad-543f-43b4-b7dd-28bac54db7dd" />

###### Vista aste per compratore
<img width="1118" height="728" alt="Schermata 2025-07-11 alle 23 24 20" src="https://github.com/user-attachments/assets/06f39ea1-ba4a-4b68-86af-78e36c5e1354" />

###### Vista asta in corso per venditore

![Senza_nome jog](https://github.com/user-attachments/assets/c5132315-f134-49a6-a8b7-0ecb2cfebb26)

###### Vista notifiche utenti
<img width="1150" height="582" alt="Schermata 2025-07-11 alle 23 27 26" src="https://github.com/user-attachments/assets/944a6109-edcd-4a45-9126-30671eacb6ec" />
