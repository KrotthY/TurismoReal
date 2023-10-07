from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.utils import IntegrityError
from .models import *
from TurismoRealApp.forms import *
import base64
from django.db.models import Q
from django.conf import settings
from django.core.files.base import ContentFile


# Función para verificar si es administrador
def es_admin(user):
    return user.is_authenticated and user.is_superuser


@user_passes_test(es_admin, login_url='index')  # Asegúrate de definir la función `es_admin` para verificar los permisos.
def panel_administracion(request):
    return render(request, 'components/administration/panel_administracion.html')
#leer (listar) los departamentos
#barra de busqueda
@user_passes_test(es_admin, login_url='index')
def listar_Dpto(request):
    q = request.GET.get('q', '')
    dptos = Dpto.objects.all()

    if q:
        dptos = dptos.filter(Q(nombre__icontains=q) | Q(descripcion__icontains=q))

    return render(request, 'components/administration/departments/listar_Dpto.html', {'dptos': dptos})

#leer (listar) los tours
@user_passes_test(es_admin, login_url='index')
def listar_Tours(request):
    q = request.GET.get('q', '')
    tours = Tour.objects.all()

    if q:
        tours = tours.filter(Q(nombre__icontains=q) | Q(descripcion__icontains=q))

    return render(request, 'components/administration/tours/listar_Tours.html', {'tours': tours})

#cambia boton activo e inactivo tour
@user_passes_test(es_admin, login_url='index')
def activaDesactiva_tour(request, id_tour):
    tour = get_object_or_404(Tour, pk=id_tour)
    # Cambiar el estado en función del estado actual
    if tour.estado == 'activo':
        tour.estado = 'inactivo'
    else:
        tour.estado = 'activo'
    
    tour.save()
    
    return redirect('listar_Traslado')

@user_passes_test(es_admin, login_url='index')
def listar_Traslado(request):
    q = request.GET.get('q', '')
    traslados = Traslado.objects.filter(Q(origen__icontains=q) | Q(destino__icontains=q))
    return render(request, 'components/administration/transfers/listar_Traslado.html', {'traslados': traslados})

@user_passes_test(es_admin, login_url='index')  # Asegúrate de definir la función `es_admin` para verificar los permisos.
def listar_usuarios(request):
    q = request.GET.get('q', '')
    
    # Admin no es visible en el panel
    usuarios = CustomUser.objects.filter(~Q(username='admin'), Q(username__icontains=q) | Q(rut__icontains=q))
    
    return render(request, 'components/administration/users/listar_Usuarios.html', {'usuarios': usuarios, 'query': q})


#cambia boton activo e inactivo traslado
@user_passes_test(es_admin, login_url='index')
def activaDesactiva_traslado(request, id_traslado):
    traslado = get_object_or_404(Traslado, pk=id_traslado)
    # Cambiar el estado en función del estado actual
    if traslado.estado == 'activo':
        traslado.estado = 'inactivo'
    else:
        traslado.estado = 'activo'
    
    traslado.save()
    
    return redirect('listar_Traslado')

#leer (listar) los reporte
@user_passes_test(es_admin, login_url='index')
def listar_Reporte(request):
    reporte = ReporteGanancias.objects.all()
    return render(request, 'components/administration/reports/listar_Reporte.html', {'reporte': reporte})
#creacion de reporte
@user_passes_test(es_admin, login_url='index')
def mostrar_reporte(request):
    reporte = ReporteGanancias.objects.all()
    return render(request, 'components/administration/reports/mostrar_reporte.html', {'reporte': reporte})

# Registro de usuarios
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirige después del registro exitoso
    else:
        form = CustomUserCreationForm()
    return render(request, 'auth/register.html', {'form': form})
# Vista de perfil
@login_required(login_url='index')
def perfil(request):
    user = request.user
    return render(request, 'auth/perfil.html', {'user': user})

# Página de inicio
def index(request):
    return render(request, 'index.html')

# Páginas de la aplicación

def galeria_departamentos(request):
    departamentos = Dpto.objects.filter(estado='activo')  
    buscar_form = BuscarCiudadForm(request.GET)

    if buscar_form.is_valid():
        busqueda = buscar_form.cleaned_data.get('busqueda')

        if busqueda:
            departamentos = departamentos.filter(
                Q(direc__ciudad__icontains=busqueda) | Q(nombre__icontains=busqueda)
            )

    return render(request, 'components/departments/galeria_departamentos.html', {'departamentos': departamentos, 'buscar_form': buscar_form})


def detalle_departamento(request, dpto_id):
    departamento = get_object_or_404(Dpto, pk=dpto_id)
    return render(request, 'components/departments/detalle_departamento.html', {'departamento': departamento})

def traslado(request):
    return render(request, 'components/transfers/traslado.html')


def galeria_tours(request):
    tours = Tour.objects.all()  # Obtén todos los departamentos desde la base de datos
    return render(request, 'components/tours/galeria_tours.html', {'tours': tours})


@user_passes_test(es_admin, login_url='index')
def crearDepartamentos(request):
    if request.method == 'POST':
        formulario = formCrearDepartamentos(request.POST, request.FILES)
        if formulario.is_valid():
            data_form = formulario.cleaned_data
            try:
                objDir = Direc(
                    calle=data_form['calle'],
                    numero=data_form['numero'],
                    ndpto=data_form['ndpto'],
                    ciudad=data_form['ciudad'],
                    region=data_form['region'],
                    pais=data_form['pais']
                )
                objDir.save()

                objDepto = Dpto(
                    nombre=data_form['nombre'],
                    descripcion=data_form['descripcion'],
                    tarifa_diaria=data_form['tarifa_diaria'],
                    direc=objDir
                )
                objDepto.save()

                # Ahora procesa las imágenes y guárdalas como objetos BLOB en Oracle
                for i in range(1, 8):
                    imagen_field_name = f'imagen_{i}'
                    if imagen_field_name in request.FILES:
                        imagen_file = request.FILES[imagen_field_name]
                        imagen_data = imagen_file.read()
                        imagen_name = imagen_file.name  # Obtén el nombre de la imagen
                        imagen_instance = ContentFile(imagen_data, name=imagen_name)
                        DptoImagen.objects.create(departamento=objDepto, imagen=imagen_instance)

                # Manejo de los servicios seleccionados
                servicios_seleccionados_nombres = request.POST.getlist('servicios')
                servicios_seleccionados = Servicio.objects.filter(nombre__in=servicios_seleccionados_nombres)
                objDepto.servicios.set(servicios_seleccionados)
                
                messages.success(request, f'Se ha creado correctamente el departamento: {objDepto.nombre}')
            except IntegrityError as e:
                messages.error(request, 'Ya existe un departamento con el mismo nombre.')

            return redirect('listar_Dpto')  # Redirige a una vista de éxito
    else:
        formulario = formCrearDepartamentos()

    return render(request, 'components/administration/departments/crear_departamento.html', {'form': formulario})

#cambia boton activo e inactivo
@user_passes_test(es_admin, login_url='index')
def activaDesactiva_departamento(request, dpto_id):
    departamento = get_object_or_404(Dpto, pk=dpto_id)
    # Cambiar el estado en función del estado actual
    if departamento.estado == 'activo':
        departamento.estado = 'inactivo'
    else:
        departamento.estado = 'activo'
    
    departamento.save()
    
    return redirect('listar_Dpto')

#acitva desactiva usuario
# Vista para activar/desactivar un usuario existente
@user_passes_test(es_admin, login_url='index')
def activaDesactiva_usuario(request, usuario_id):
    usuario = get_object_or_404(CustomUser, pk=usuario_id)
    
    # Cambiar el estado en función del estado actual
    if usuario.estado == 'activo':
        usuario.estado = 'inactivo'
    else:
        usuario.estado = 'activo'
    
    usuario.save()
    
    # Redirigir a la página de listar usuarios
    return redirect('listar_Usuarios')

# Crear tours
@user_passes_test(es_admin, login_url='index')
def crear_tours(request):
    if request.method == 'POST':
        form = TourCreationForm(request.POST)
        if form.is_valid():
            # Guardar el nuevo tour en la base de datos
            objTour = form.save(commit=False)
            # Personaliza el tour antes de guardarlo si es necesario
            # Por ejemplo, puedes establecer un usuario propietario si está disponible en el contexto
            if request.user.is_authenticated:
                objTour.customUser = request.user  # Asigna el usuario actual al tour si está autenticado
            objTour.save()
            messages.success(request, f'El tour {objTour.nombre} creó con éxito.')
            # Redireccionar a la página de detalles del tour recién creado o a donde desees
            return redirect('listar_Tours')
    else:
        form = TourCreationForm()
        
    return render(request, 'components/administration/tours/crear_tours.html', {'form': form})

#creacion de traslado
@user_passes_test(es_admin, login_url='index')
def crear_traslado(request):
    if request.method == 'POST':
        form = TrasladoCreationForm(request.POST)
        if form.is_valid():        
            # Guardar el nuevo traslado en la base de datos
            traslado = form.save(commit=False)
            # Personalizar el traslado antes de guardarlo si es necesario
            # Por ejemplo, puedes establecer un usuario propietario si está disponible en el contexto
            if request.user.is_authenticated:
                traslado.customUser = request.user  # Asigna el usuario actual al traslado si está autenticado
            traslado.save()
            messages.success(request, 'El traslado se creó con éxito.')
            # Redireccionar a la página de detalles del traslado recién creado o a donde desees
            return redirect('listar_Traslado')
    else:
        form = TrasladoCreationForm()

    return render(request, 'components/administration/transfers/crear_traslado.html', {'form': form})

# Vista para listar todos los servicios
@user_passes_test(es_admin, login_url='index')
def listar_servicios(request):
    q = request.GET.get('q', '')
    servicios = Servicio.objects.filter(Q(nombre__icontains=q))
    return render(request, 'components/administration/services/listar_servicios.html', {'servicios': servicios, 'query': q})

#crear servicio
@user_passes_test(es_admin, login_url='index')
def crear_servicio(request):
    if request.method == 'POST':
        form = ServicioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_servicios')
    else:
        form = ServicioForm()
    return render(request, 'components/administration/services/crear_servicio.html', {'form': form})


@user_passes_test(es_admin, login_url='index')  # Asegúrate de definir la función `es_admin` para verificar los permisos.
def crear_equipamiento(request):
    if request.method == 'POST':
        form = EquipamientoForm(request.POST)
        if form.is_valid():
            # Guarda el formulario si es válido
            form.save()
            return redirect('listar_Equipamiento')  # Reemplaza 'listar_inventario' con la URL correcta
    else:
        form = EquipamientoForm()

    return render(request, 'components/administration/equipment/crear_Equipamiento.html', {'form': form})

#actualizar servicio
@user_passes_test(es_admin, login_url='index')
def actualizar_servicio(request, servicio_id):
    # Obtener el servicio que se desea actualizar desde la base de datos
    servicio = get_object_or_404(Servicio, id=servicio_id)

    if request.method == 'POST':
        # Si el formulario se envía con datos, procesar los datos
        formulario = ServicioForm(request.POST, instance=servicio)

        if formulario.is_valid():
            # Guardar los cambios en el servicio
            formulario.save()

            # Redirigir a la página de lista de servicios o a donde desees
            return redirect('listar_servicios')
    else:
        # Si es una solicitud GET, mostrar el formulario con los datos actuales del servicio
        formulario = ServicioForm(instance=servicio)

    return render(request, 'components/administration/services/actualizar_servicio.html', {'formulario': formulario})

# Vista para activar/desactivar un servicio existente
@user_passes_test(es_admin, login_url='index')
def activaDesactiva_servicio(request, servicio_id):
    servicio = get_object_or_404(Servicio, pk=servicio_id)
    # Cambiar el estado en función del estado actual
    if servicio.estado == 'activo':
        servicio.estado = 'inactivo'
    else:
        servicio.estado = 'activo'
    
    servicio.save()
    
    return redirect('listar_servicios')

#listar equipamiento
@user_passes_test(es_admin, login_url='index')
def listar_equipamiento(request):
    q = request.GET.get('q', '')
    equipamientos = Equipamiento.objects.filter(Q(objeto__icontains=q))
    return render(request, 'components/administration/equipment/listar_Equipamiento.html', {'equipamientos': equipamientos, 'query': q})



@user_passes_test(es_admin, login_url='index')  
def activa_desactiva_equipamiento(request, id_equipamiento):
    equipamiento_instance = get_object_or_404(Equipamiento, pk=id_equipamiento)
    
    # Cambiar el estado en función del estado actual
    if equipamiento_instance.estado == 'activo':
        equipamiento_instance.estado = 'inactivo'
    else:
        equipamiento_instance.estado = 'activo'
    
    equipamiento_instance.save()
    
    return redirect('listar_Equipamiento')


