# Generated by Django 5.0.1 on 2024-01-27 03:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservas', '0009_cargo_genero_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='cargo',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='user',
            name='genero',
            field=models.CharField(max_length=30),
        ),
    ]
