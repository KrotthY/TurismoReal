"""TurismoReal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path, include
import TurismoRealApp.views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    #index
    path('inicio/',TurismoRealApp.views.index, name='index'),
    path( '',TurismoRealApp.views.index, name='index'),
    path( 'index/',TurismoRealApp.views.index, name='index'),
    path( 'perfil/',TurismoRealApp.views.perfil, name='perfil'),
    
    #menu admin
    path( 'panel_administracion/',TurismoRealApp.views.panel_administracion, name='panel_administracion'),#read
    #usuario
    path( 'listar_Usuarios/',TurismoRealApp.views.listar_usuarios, name='listar_Usuarios'),#read
    path('usuarios/<int:usuario_id>/eliminar/', TurismoRealApp.views.activaDesactiva_usuario, name='activa_desactiva_usuario'),
    #crud traslado
    path( 'crear_traslado/',TurismoRealApp.views.crear_traslado, name='crear_traslado'),#create
    path( 'listar_Traslado/',TurismoRealApp.views.listar_Traslado, name='listar_Traslado'),#read
    path('traslado/<int:id_traslado>/eliminar/', TurismoRealApp.views.activaDesactiva_traslado, name='activa_desactiva_traslado'),#boton estado
    #crud tour
    path( 'crear_tours/',TurismoRealApp.views.crear_tours, name='crear_tours'),#create
    path( 'listar_Tours/',TurismoRealApp.views.listar_Tours, name='listar_Tours'),#read
    path('tours/<int:id_tour>/eliminar/', TurismoRealApp.views.activaDesactiva_tour, name='activa_desactiva_tour'),#boton estado
    #crud dpto
    path( 'crear_departamento/',TurismoRealApp.views.crearDepartamentos, name='crear_departamento'),#create
    path( 'listar_Dpto/',TurismoRealApp.views.listar_Dpto, name='listar_Dpto'),#read
    path('departamentos/<int:dpto_id>/eliminar/', TurismoRealApp.views.activaDesactiva_departamento, name='activa_desactiva_departamento'),#boton estado
    #crud servicio
    path( 'crear_servicio/',TurismoRealApp.views.crear_servicio, name='crear_servicio'),#create
    path( 'listar_servicios/',TurismoRealApp.views.listar_servicios, name='listar_servicios'),#read
    path('servicios/<int:servicio_id>/eliminar/', TurismoRealApp.views.activaDesactiva_servicio, name='activa_desactiva_servicio'),
    path('servicios/<int:servicio_id>/', TurismoRealApp.views.actualizar_servicio, name='actualizar_servicio'), #update
    #crud reporte
    path( 'listar_Reporte/',TurismoRealApp.views.listar_Reporte, name='listar_Reporte'),#read
    path( 'mostrar_reporte/',TurismoRealApp.views.mostrar_reporte, name='mostrar_reporte'),#read unitario generar automaticamente en pl
    #crud equipamiento
    path( 'crear_Equipamiento/',TurismoRealApp.views.crear_equipamiento, name='crear_Equipamiento'),#create
    path( 'listar_Equipamiento/',TurismoRealApp.views.listar_equipamiento, name='listar_Equipamiento'),#read
    path('equipamiento/<int:id_equipamiento>/eliminar/', TurismoRealApp.views.activa_desactiva_equipamiento, name='activa_desactiva_equipamiento'),
    #vista cliente
    path( 'galeria_departamentos/',TurismoRealApp.views.galeria_departamentos, name='galeria_departamentos'),
    path('departamento/<int:dpto_id>/', TurismoRealApp.views.detalle_departamento, name='detalle_departamento'),

    path( 'traslado/',TurismoRealApp.views.traslado, name='traslado'),
    path( 'galeria_tours/',TurismoRealApp.views.galeria_tours, name='galeria_tours'),
    #login
    path( 'accounts/', include('django.contrib.auth.urls')),
    #registrar cuenta
    path('register/', TurismoRealApp.views.register, name='register'),
    ]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)