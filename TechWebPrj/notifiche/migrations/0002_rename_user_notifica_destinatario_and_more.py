# Generated by Django 5.2.3 on 2025-07-10 23:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifiche', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notifica',
            old_name='user',
            new_name='destinatario',
        ),
        migrations.RemoveField(
            model_name='notifica',
            name='message',
        ),
        migrations.RemoveField(
            model_name='notifica',
            name='reply_to',
        ),
        migrations.AddField(
            model_name='notifica',
            name='messaggio',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='notifica',
            name='titolo',
            field=models.CharField(default='Nuovo messaggio', max_length=255),
        ),
    ]
