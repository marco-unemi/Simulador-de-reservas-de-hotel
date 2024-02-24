from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import get_template
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db import IntegrityError
from django.http import HttpResponse, JsonResponse
from .models import Hotel, Habitacion, Reserva, Pedido, Usuario
from .forms import HotelForm, HabitacionForm, ReservaForm, PedidoForm, RegistroForm, LoginForm, CambiarPasswordForm
from io import BytesIO
from xhtml2pdf import pisa


# Create your views here.
def home(request):
    return render(request, 'index.html')


def signup(request):
    if request.method == 'POST':
        registroForm = RegistroForm(request.POST)
        if registroForm.is_valid():
            cedula = registroForm.cleaned_data['cedula']
            first_name = registroForm.cleaned_data['first_name']
            last_name = registroForm.cleaned_data['last_name']
            fecha_de_nacimiento = registroForm.cleaned_data['fecha_de_nacimiento']
            genero = registroForm.cleaned_data['genero']
            email = registroForm.cleaned_data['email']
            telefono = registroForm.cleaned_data['telefono']
            cargo = registroForm.cleaned_data['cargo']

            username = registroForm.cleaned_data['username']
            password1 = registroForm.cleaned_data['password1']
            password2 = registroForm.cleaned_data['password2']

            if password1 == password2:
                try:
                    user = Usuario.objects.create_user(
                        cedula=cedula,
                        first_name=first_name,
                        last_name=last_name,
                        fecha_de_nacimiento=fecha_de_nacimiento,
                        genero=genero,
                        email=email,
                        username=username,
                        telefono=telefono,
                        cargo=cargo,
                        password=password1,
                    )
                    user.save()
                    login(request, user)
                    return redirect('reserva')
                except IntegrityError:
                    return render(request, 'signin.html', {
                        'form': LoginForm(),
                        'error_message': 'Username ya existe!.'
                    })
            else:
                return HttpResponse('Las contraseñas no coinciden!')
        else:
            return HttpResponse(f"Formulario no válido: {registroForm.errors}")
    else:
        registroForm = RegistroForm()
        return render(request, 'signup.html', {
            'registroForm': registroForm,
        })


def cerrar_sesion(request):
    logout(request)
    return redirect('home')


def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': LoginForm(),
        })
    else:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('reserva')
        else:
            return render(request, 'signin.html', {
                'form': LoginForm(),
                'error_message': 'Username or password is incorrect.'
            })


def reserva(request):
    habitaciones = Habitacion.objects.all()

    return render(request, 'reserva.html', {
        'habitaciones': habitaciones,
    })


def reservar_habitacion(request, habitacion_id):
    habitacion = get_object_or_404(Habitacion, pk=habitacion_id)

    if request.method == 'POST':
        formReserva = ReservaForm(request.POST)
        if formReserva.is_valid():
            reserva = formReserva.save(commit=False)
            habitacion.reservada = True
            habitacion.save()
            reserva.save()

            return redirect('reserva')
        else:
            return HttpResponse(f"Formulario no válido: {formReserva.errors}")

    else:
        formReserva = ReservaForm()
        return render(request, 'reservar_Habitacion.html', {
            'habitacion': habitacion,
            'formReserva': formReserva,
        })


def punto_venta(request):
    if request.method == 'POST':
        form = PedidoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('punto_venta')
        else:
            habitaciones = Habitacion.objects.filter(reservada=True)
            reservas = Reserva.objects.all()
            return render(request, 'punto_venta.html', {
                'form': form,
                'habitaciones': habitaciones,
                'reservas': reservas,
            })
    else:
        habitaciones = Habitacion.objects.filter(reservada=True)
        reservas = Reserva.objects.all()
        form = PedidoForm()
        return render(request, 'punto_venta.html', {
            'form': form,
            'habitaciones': habitaciones,
            'reservas': reservas,
        })


def obtener_cliente(request, habitacion_id):
    reserva = Reserva.objects.filter(habitacion_id=habitacion_id).last()
    cliente = reserva.cliente if reserva else ""
    return JsonResponse({'cliente': cliente})


def factura_pdf(request, reserva_id):
    try:
        # Obtener la reserva del cliente
        reserva_cliente = get_object_or_404(Reserva, pk=reserva_id)

        # Verificar si la habitación asociada a la reserva está reservada
        habitacion_reservada = reserva_cliente.habitacion.reservada

        # Obtener pedidos asociados con el cliente de la reserva
        pedidos = Pedido.objects.filter(cliente=reserva_cliente.cliente)

        # Si la habitación está reservada, aplicar el filtro
        if habitacion_reservada:
            pedidos = pedidos.filter(habitacion=reserva_cliente.habitacion)

        # Obtener todos los hoteles
        hotel = Hotel.objects.all()

        subtotal = reserva_cliente.total_pagar

        for total_pedido in pedidos:
            subtotal += total_pedido.total_pagar

        impuesto = round(subtotal * 0.05, 2)

        monto = subtotal + impuesto

        print(subtotal)
        print(impuesto)
        print(monto)

        fecha_actual = timezone.now().strftime('%d/%m/%Y')

        context_dict = {
            'reserva_cliente': reserva_cliente,
            'hotel': hotel,
            'pedidos': pedidos,
            'subtotal': subtotal,
            'impuesto': impuesto,
            'monto': monto,
            'fecha_actual': fecha_actual,
        }

        template_src = 'factura_pdf.html'
        template = get_template(template_src)
        html = template.render(context_dict)
        result = BytesIO()

        pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)

        if not pdf.err:
            # Llamar a la función de verificación de salida para actualizar el estado de las habitaciones
            verificacion_de_salida(reserva_cliente)
            pedidos.delete()
            reserva_cliente.delete()
            return HttpResponse(result.getvalue(), content_type='application/pdf')

    except Exception as e:
        return HttpResponse(f'Error en la generación de la factura: {e}', status=500)


def verificacion_de_salida(reserva):
    habitaciones_reservadas = Habitacion.objects.filter(reserva=reserva)
    habitaciones_reservadas.update(reservada=False)


def facturas(request):
    # habitacion__reservada=True
    reservas = Reserva.objects.filter()
    if request.method == 'GET' and 'cedula' in request.GET:
        cedula = request.GET['cedula']
        reservas = Reserva.objects.filter(cedula__icontains=cedula)
    else:
        reservas = Reserva.objects.all()
    return render(request, 'facturas.html', {
        'reservas': reservas,
    })


def usuarios(request):
    usuarios = Usuario.objects.all()
    user_log = request.user
    return render(request, 'usuarios.html', {
        'usuarios': usuarios,
        'user_log': user_log
    })


def informacion_hotel(request):
    hotel = Hotel.objects.all().first()

    if request.method == 'POST':
        fromHotel = HotelForm(request.POST, instance=hotel)
        if fromHotel.is_valid():
            hotel = fromHotel.save(commit=False)
            hotel.save()
            return redirect('informacion_hotel')
        else:
            print(f"Formulario no válido: {fromHotel.errors}")
    else:
        fromHotel = HotelForm(instance=hotel)
        return render(request, 'informacion_hotel.html', {
            'hotel': hotel,
            'fromHotel': fromHotel,
        })


def habitaciones(request):
    if request.method == 'POST':
        formHabitacion = HabitacionForm(request.POST)
        if formHabitacion.is_valid():
            habitacion = formHabitacion.save(commit=False)
            habitacion.save()
            return redirect('habitaciones')
        else:
            print(f"Formulario no válido: {formHabitacion.errors}")
    else:
        formHabitacion = HabitacionForm()
        habitaciones = Habitacion.objects.all()

        siguiente_numero_de_habitacione = habitaciones.count() + 1

        return render(request, 'habitaciones.html', {
            'formHabitacion': formHabitacion,
            'habitaciones': habitaciones,
            'siguiente_numero_de_habitacione': siguiente_numero_de_habitacione,
        })


def editar_habitacion(request, habitacion_id):
    habitacion = get_object_or_404(Habitacion, pk=habitacion_id)
    if request.method == 'POST':
        formHabitacion = HabitacionForm(request.POST, instance=habitacion)
        if formHabitacion.is_valid():
            habitacion_editada = formHabitacion.save(commit=False)
            habitacion_editada.save()
            return redirect('habitaciones')
        else:
            return HttpResponse(f"Formulario no válido: {formHabitacion.errors}")
    else:
        formHabitacion = HabitacionForm(instance=habitacion)
    return render(request, 'editar_habitacion.html', {
        'formHabitacion': formHabitacion,
        'habitacion': habitacion,
    })


def eliminar_habitacion(request, habitacion_id):
    habitacion = get_object_or_404(Habitacion, pk=habitacion_id)
    if request.method == 'POST':
        habitacion.delete()
        return redirect('habitaciones')


@login_required
def perfil(request):
    user = request.user
    return render(request, 'perfil.html', {'user': user})


def fact(request, reserva_id):
    # Obtener la reserva del cliente
    reserva_cliente = get_object_or_404(Reserva, pk=reserva_id)

    # Verificar si la habitación asociada a la reserva está reservada
    habitacion_reservada = reserva_cliente.habitacion.reservada

    # Obtener pedidos asociados con el cliente de la reserva
    pedidos = Pedido.objects.filter(cliente=reserva_cliente.cliente)

    # Si la habitación está reservada, aplicar el filtro
    if habitacion_reservada:
        pedidos = pedidos.filter(habitacion=reserva_cliente.habitacion)

    # Obtener todos los hoteles
    hotel = Hotel.objects.all()

    subtotal = reserva_cliente.total_pagar

    for total_pedido in pedidos:
        subtotal += total_pedido.total_pagar

    impuesto = round(subtotal * 0.05, 2)

    monto = subtotal + impuesto

    print(subtotal)
    print(impuesto)
    print(monto)

    fecha_actual = timezone.now().strftime('%d/%m/%Y')

    return render(request, 'fact.html', {
        'reserva_cliente': reserva_cliente,
        'hotel': hotel,
        'pedidos': pedidos,
        'subtotal': subtotal,
        'impuesto': impuesto,
        'monto': monto,
        'fecha_actual': fecha_actual,
    })
    
    
def editar_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, pk=usuario_id)
    
    if request.method == 'POST':
        registroForm = RegistroForm(request.POST, instance=usuario)
        if registroForm.is_valid():
            registroForm.save()
            return redirect('editar_usuario', usuario.id)
        else:
            return HttpResponse(f"Formulario no válido: {registroForm.errors}")
        
    else:
        registroForm = RegistroForm(instance=usuario)
        
    return render(request, 'editar_usuario.html', {
        'registroForm': registroForm,
        'usuario': usuario,
    })
    
    
def eliminar_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, pk=usuario_id)
    if request.method == 'POST':
        usuario.delete()
        return redirect('usuarios')
    else:
        return render(request, 'eliminar_usuario.html', {
            'usuario': usuario
        })
   
   
def agregar_usuarios(request):
    if request.method == 'POST':
        registroForm = RegistroForm(request.POST)
        if registroForm.is_valid():
            cedula = registroForm.cleaned_data['cedula']
            first_name = registroForm.cleaned_data['first_name']
            last_name = registroForm.cleaned_data['last_name']
            fecha_de_nacimiento = registroForm.cleaned_data['fecha_de_nacimiento']
            genero = registroForm.cleaned_data['genero']
            email = registroForm.cleaned_data['email']
            telefono = registroForm.cleaned_data['telefono']
            cargo = registroForm.cleaned_data['cargo']

            username = registroForm.cleaned_data['username']
            password1 = registroForm.cleaned_data['password1']
            password2 = registroForm.cleaned_data['password2']

            if password1 == password2:
                try:
                    user = Usuario.objects.create_user(
                        cedula=cedula,
                        first_name=first_name,
                        last_name=last_name,
                        fecha_de_nacimiento=fecha_de_nacimiento,
                        genero=genero,
                        email=email,
                        username=username,
                        telefono=telefono,
                        cargo=cargo,
                        password=password1,
                    )
                    user.save()
                    return redirect('usuarios')
                except IntegrityError:
                    registroForm = RegistroForm()
                    return render(request, 'agregar_usuarios.html', {
                        'error_message': 'Username ya existe!.'
                    })
            else:
                return HttpResponse('Las contraseñas no coinciden!')
        else:
            return HttpResponse(f"Formulario no válido: {registroForm.errors}")
    else:
        registroForm = RegistroForm()
        return render(request, 'agregar_usuarios.html', {
            'registroForm': registroForm,
        })
        

def cambiar_password(request, usuario_id):
    user = get_object_or_404(Usuario, pk=usuario_id)
    
    if request.method == 'POST':
        form = CambiarPasswordForm(request.POST)
        if form.is_valid():
            user.set_password(form.cleaned_data.get('password1'))
            user.save()
            return redirect('editar_usuario', user.id)
        else:
            return HttpResponse(f"Formulario no válido: {form.errors}")
    else:           
        form = CambiarPasswordForm()

    return render(request, 'cambiar_password.html', {
        'usuario': user,
        'form': form
    })