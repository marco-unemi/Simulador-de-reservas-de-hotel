# Generated by Django 5.0.1 on 2024-02-20 23:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservas', '0022_remove_pedido_facturado_reserva_reserva_terminada'),
    ]

    operations = [
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cedula', models.CharField(max_length=10)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('fechaNacimiento', models.DateField()),
                ('genero', models.CharField(choices=[('', '-----'), ('fenemino', 'FEMENINO'), ('masculino', 'MASCULINO')], max_length=9)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('username', models.CharField(max_length=30)),
                ('password', models.CharField(max_length=20)),
                ('telefono', models.CharField(max_length=15)),
                ('date_joined', models.DateTimeField(auto_now=True)),
                ('cargo', models.CharField(choices=[('', '-----'), ('gerente', 'GERENTE'), ('admin', 'ADMINISTRADOR'), ('empleado', 'EMPLEADO')], max_length=8)),
                ('last_login', models.DateTimeField(auto_now=True)),
                ('status', models.BooleanField(default=True)),
            ],
        ),
    ]
