# Generated by Django 5.2.3 on 2025-07-09 17:22

import aste.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aste', '0002_remove_asta_image_allegato'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allegato',
            name='immagine',
            field=models.ImageField(upload_to=aste.models.Allegato.upload_to_per_asta),
        ),
        migrations.AlterField(
            model_name='asta',
            name='descrizione',
            field=models.TextField(),
        ),
    ]
