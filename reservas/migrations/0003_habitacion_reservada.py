# Generated by Django 5.0.1 on 2024-01-24 01:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservas', '0002_habitacion'),
    ]

    operations = [
        migrations.AddField(
            model_name='habitacion',
            name='reservada',
            field=models.BooleanField(default=False),
        ),
    ]