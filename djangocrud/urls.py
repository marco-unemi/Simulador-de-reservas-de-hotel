"""
URL configuration for djangocrud project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from reservas import views 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('reserva/', views.reserva, name='reserva'),
    path('reserva/reservar_habitacion/<int:habitacion_id>/', views.reservar_habitacion, name='reservar_habitacion'),
    path('punto_venta/', views.punto_venta, name='punto_venta'),
    path('facturas/', views.facturas, name='facturas'),
    path('facturas/factura_pdf/<int:reserva_id>/', views.factura_pdf, name='factura_pdf'),
    path('facturas/fact/<int:reserva_id>/', views.fact, name='fact'),
    path('usuarios/', views.usuarios, name='usuarios'),
    path('informacion_hotel/', views.informacion_hotel, name='informacion_hotel'),
    path('habitaciones/', views.habitaciones, name='habitaciones'),
    path('habitaciones/editar_habitacion/<int:habitacion_id>/', views.editar_habitacion, name='editar_habitacion'),
    path('habitaciones/eliminar_habitacion/<int:habitacion_id>/', views.eliminar_habitacion, name='eliminar_habitacion'),
    path('perfil/', views.perfil, name='perfil'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('cerrar_sesion/', views.cerrar_sesion, name='cerrar_sesion'),
    path('obtener_cliente/<int:habitacion_id>/', views.obtener_cliente, name='obtener_cliente'),
    path('editar_usuario/<int:usuario_id>/', views.editar_usuario, name='editar_usuario'),
    path('editar_usuario/cambiar_password/<int:usuario_id>/', views.cambiar_password, name='cambiar_password'),
    path('eliminar_usuario/<int:usuario_id>/', views.eliminar_usuario, name='eliminar_usuario'),
    path('agregar_usuarios/', views.agregar_usuarios, name='agregar_usuarios'),
]
