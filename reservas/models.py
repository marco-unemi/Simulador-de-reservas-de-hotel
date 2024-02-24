from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


# Create your models here.

class UsuarioManager(BaseUserManager):
    def create_user(self, cedula, first_name, last_name, fecha_de_nacimiento, genero, email, username, telefono, cargo, password=None):
        if not email:
            raise ValueError('El usuario debe tener un correoelectronico!')

        user = self.model(
            cedula = cedula,
            first_name = first_name,
            last_name = last_name,
            fecha_de_nacimiento = fecha_de_nacimiento,
            genero = genero,
            email = self.normalize_email(email),
            username = username,
            telefono = telefono,
            cargo = cargo,
        )
        user.set_password(password)
        user.save()
        return user


    def create_superuser(self, cedula, first_name, last_name, fecha_de_nacimiento, genero, email, username, telefono, cargo, password):
        user = self.create_user(
            cedula = cedula,
            first_name = first_name,
            last_name = last_name,
            fecha_de_nacimiento = fecha_de_nacimiento,
            genero = genero,
            email = email,
            username = username,
            telefono = telefono,
            cargo = cargo,
            password = password,
        )
        user.user_admin = True
        user.is_staff = True
        user.save()
        return user


class Usuario(AbstractBaseUser):
    # datos personales
    cedula = models.CharField(max_length=10, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    fecha_de_nacimiento = models.DateField()
    OPCIONES_GENERO = [
        ('', '-----'),
        ('FEMENINO', 'FEMENINO'),
        ('MASCULINO', 'MASCULINO'),
    ]
    genero = models.CharField(max_length=10, choices=OPCIONES_GENERO)

    # datos de la cuenta
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, unique=True)
    telefono = models.CharField(max_length=15)

    # datos del empleo
    fecha_de_ingreso = models.DateTimeField(auto_now=True)
    OPCIONES_ROL = [
        ('', '-----'),
        ('GERENTE', 'GERENTE'),
        ('ADMINISTRADOR', 'ADMINISTRADOR'),
        ('EMPLEADO', 'EMPLEADO')
    ]
    cargo = models.CharField(max_length=13, choices=OPCIONES_ROL)
    last_login = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    user_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = [
        'cedula', 'first_name', 'last_name', 'fecha_de_nacimiento', 'genero', 'email', 'telefono', 'fecha_de_ingreso', 'cargo'
    ]

    objects = UsuarioManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def if_staff(self):
        return self.user_admin


class Hotel(models.Model):
    nombre = models.CharField(max_length=255)
    telefono = models.CharField(max_length=20)
    correo = models.EmailField()
    ubicacion = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre


class Habitacion(models.Model):
    nombre = models.CharField(max_length=100)
    numero = models.IntegerField(default=0)
    precio = models.FloatField(default=0)
    reservada = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.nombre} - No.{self.numero}'


class Reserva(models.Model):
    cedula = models.CharField(max_length=20)
    cliente = models.CharField(max_length=50)
    telefono = models.CharField(max_length=20)
    email = models.EmailField()
    tipo_cliente = models.CharField(max_length=20)
    habitacion = models.ForeignKey(Habitacion, on_delete=models.CASCADE)
    fecha_reserva = models.DateField()
    precio_habitacion = models.FloatField(default=0)
    tiempo = models.FloatField(default=0)
    tipo_pago = models.CharField(max_length=20)
    numero_tarjeta = models.CharField(max_length=30, default=None)
    total_pagar = models.FloatField(default=0)
    reserva_terminada = models.BooleanField(default=False)

    def __str__(self):
        return f'Habitación {self.habitacion} reservada por {self.cliente}'


class Pedido(models.Model):
    habitacion = models.ForeignKey(Habitacion, on_delete=models.CASCADE)
    cliente = models.CharField(max_length=50)
    producto = models.CharField(max_length=50)
    precio = models.FloatField(default=0)
    cantidad = models.IntegerField(default=0)
    tipo_pago = models.CharField(max_length=20)
    numero_tarjeta = models.CharField(max_length=30, default=None)
    total_pagar = models.FloatField(default=None)

    def __str__(self):
        return f'{self.producto} pedido por {self.cliente} en habitacion No.{self.habitacion}'
