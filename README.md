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

###### Vista aste per compratore

###### Vista asta in corso per venditore

###### Vista notifiche utenti
