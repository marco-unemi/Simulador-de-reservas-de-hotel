from django.contrib import admin
from .models import Hotel, Habitacion, Reserva, Pedido, Usuario


# Register your models here.
admin.site.register(Hotel)
admin.site.register(Habitacion)
admin.site.register(Reserva)
admin.site.register(Pedido)
admin.site.register(Usuario)
