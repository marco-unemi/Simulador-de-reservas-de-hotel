# Generated by Django 5.0.1 on 2024-01-29 04:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservas', '0014_alter_user_fechanacimiento'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='apellidos',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='nombres',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]
