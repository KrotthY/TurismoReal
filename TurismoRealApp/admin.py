from django.contrib import admin
from .models import *

class DptoAdmin(admin.ModelAdmin):
    search_fields = ['nombre', 'tarifa_diaria']
    list_filter = ['nombre', 'tarifa_diaria']
    list_display = ['nombre', 'descripcion', 'tarifa_diaria']
    ordering = ['nombre', 'tarifa_diaria']

class EquipamientoAdmin(admin.ModelAdmin):
    search_fields = ['objeto', 'estado']
    list_filter = ['objeto', 'estado']
    list_display = ['objeto', 'estado', 'valor']
    ordering = ['objeto', 'estado']

class TourAdmin(admin.ModelAdmin):
    search_fields = ['nombre', 'duracion', 'valor']
    list_display = ['nombre', 'duracion', 'valor']
    ordering = ['nombre', 'duracion']

class TrasladoAdmin(admin.ModelAdmin):
    search_fields = ['origen', 'destino', 'valor']
    list_filter = ['origen', 'destino']
    list_display = ['origen', 'destino', 'valor']
    ordering = ['origen', 'destino']

class CheckOutAdmin(admin.ModelAdmin):
    search_fields = ['fecha_check_out', 'reserva_id_reserva']
    list_display = ['fecha_check_out', 'reserva_id_reserva', 'costos_reparacion']
    ordering = ['fecha_check_out']

admin.site.register(CustomUser)
admin.site.register(Multa)
admin.site.register(CheckIn)
admin.site.register(CheckOut, CheckOutAdmin)
admin.site.register(Reserva)
admin.site.register(Dpto, DptoAdmin)
admin.site.register(Direc)
admin.site.register(Equipamiento, EquipamientoAdmin)
admin.site.register(Mantencion)
admin.site.register(ReporteGanancias)
admin.site.register(Tour, TourAdmin)
admin.site.register(Traslado, TrasladoAdmin)
