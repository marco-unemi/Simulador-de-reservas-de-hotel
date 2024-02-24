from django.forms import ModelForm
from .models import Hotel, Habitacion, Reserva, Pedido, Usuario
from django import forms
from django.contrib.auth.forms import AuthenticationForm


class HotelForm(ModelForm):
    class Meta:
        model = Hotel
        fields = [
            'nombre', 'telefono', 'correo', 'ubicacion'
            ]

class HabitacionForm(ModelForm):
    class Meta:
        model = Habitacion
        fields = [
            'nombre', 'numero', 'precio'
            ]
        
class ReservaForm(ModelForm):
    class Meta:
        model = Reserva
        fields = [
            'cedula', 'cliente', 'telefono', 'email', 'tipo_cliente', 'habitacion', 'fecha_reserva', 'precio_habitacion', 'tiempo', 'tipo_pago', 'numero_tarjeta', 'total_pagar'
        ]
        
class PedidoForm(ModelForm):
    class Meta:
        model = Pedido
        fields = [
            'habitacion', 'cliente', 'producto', 'precio', 'cantidad', 'tipo_pago', 'numero_tarjeta', 'total_pagar'
        ]

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args,**kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Usuario'
        self.fields['password'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['placeholder'] = 'Contraseña'
        
class RegistroForm(forms.ModelForm):
    """ Formulario de Registro de un Usuario en la base de datos

        Variables:

            - password1:    Contraseña
            - password2:    Verificación de la contraseña

    """
    password1 = forms.CharField(label = 'Contraseña',widget = forms.PasswordInput(
        attrs = {
            'class': 'form-control',
            'placeholder': 'Ingrese su contraseña...',
            'id': 'password1',
            'required':'required',
        }
    ))

    password2 = forms.CharField(label = 'Contraseña de Confirmación', widget = forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese nuevamente su contraseña...',
            'id': 'password2',
            'required': 'required',
        }
    ))
    
    class Meta:
        model = Usuario
        fields = [
            'cedula', 'first_name', 'last_name', 'fecha_de_nacimiento', 'genero', 
            'email', 'username',
            'telefono', 'cargo',
        ]
        

class CambiarPasswordForm(forms.Form):
    password1 = forms.CharField(label = 'Contraseña',widget = forms.PasswordInput(
        attrs = {
            'class': 'form-control',
            'placeholder': 'Ingrese su nueva contraseña...',
            'id': 'id_password1',
            'required':'required',
        }
    ))

    password2 = forms.CharField(label = 'Contraseña de Confirmación', widget = forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese nuevamente la nueva contraseña...',
            'id': 'id_password2',
            'required': 'required',
        }
    ))