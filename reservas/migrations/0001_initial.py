# Generated by Django 5.0.1 on 2024-01-22 21:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Hotel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
                ('telefono', models.CharField(max_length=20)),
                ('correo', models.EmailField(max_length=254)),
                ('ubicacion', models.CharField(max_length=255)),
            ],
        ),
    ]
