# Generated by Django 5.0.1 on 2024-01-29 03:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservas', '0013_remove_user_apellidos_remove_user_nombres_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='fechaNacimiento',
            field=models.DateField(blank=True, null=True),
        ),
    ]