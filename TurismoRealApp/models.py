from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    rut = models.CharField(max_length=20, unique=True)
    telefono = models.CharField(max_length=20)
    estado = models.CharField(max_length=20, default='activo')
    
    class Meta:
        db_table = 'usuario'
        
class Equipamiento(models.Model):
    id_equipamiento = models.AutoField(primary_key=True)
    objeto = models.CharField(max_length=250)
    valor = models.IntegerField()
    estado = models.CharField(max_length=20, default='activo')

    class Meta:
        db_table = 'equipamiento'  
        
class Multa(models.Model):
    id = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=1000)
    monto = models.IntegerField()
    estado = models.CharField(max_length=20, default='activo')
    check_out = models.ForeignKey(
        'checkOut',
        on_delete=models.CASCADE,
        related_name='multas'
    )
    class Meta:
        db_table = 'multa'

class CheckIn(models.Model):
    id_check_in = models.AutoField(primary_key=True)
    fecha_check_in = models.DateField()
    pago_restante = models.IntegerField()
    firma_cliente = models.CharField(max_length=1000)
    estado = models.CharField(max_length=20, default='activo')
    reserva = models.ForeignKey(
        'reserva',
        on_delete=models.CASCADE,
        related_name='check_ins'
    )
    class Meta:
        db_table = 'checkin'

class CheckOut(models.Model):
    id_check_out = models.AutoField(primary_key=True)
    fecha_check_out = models.DateField()
    costos_reparacion = models.IntegerField()
    firma_funcionario = models.CharField(max_length=1000)
    multas_id = models.IntegerField(null=True)
    reserva_id_reserva = models.IntegerField()
    estado = models.CharField(max_length=20, default='activo')

    reserva = models.ForeignKey(
        'reserva',
        on_delete=models.CASCADE,
        null=True,
        related_name='check_outs'
    )
    class Meta:
        db_table = 'checkout'

class Reserva(models.Model):
    id_reserva = models.AutoField(primary_key=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    monto_total = models.IntegerField()
    cantidad_personas = models.IntegerField()
    estado = models.CharField(max_length=20, default='activo')
    
    customUser = models.ForeignKey(
        'customUser',
        on_delete=models.SET_NULL,
        null=True,
        related_name='reservas'
    )
    dpto = models.ForeignKey(
        'dpto',
        on_delete=models.CASCADE,
        null=True,
        related_name='reservas'
    )
    class Meta:
        db_table = 'reserva'


class Servicio(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    estado = models.CharField(max_length=20, default='activo')
    def __str__(self):
        return self.nombre
    class Meta:
        db_table = 'servicio'
    

class Dpto(models.Model):
    id_dpto = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=20, unique=True)
    descripcion = models.CharField(max_length=250)
    tarifa_diaria = models.IntegerField()
    estado = models.CharField(max_length=20, default='activo')
    direc = models.ForeignKey(
        'direc',
        on_delete=models.CASCADE,
        null=True,
        related_name='dptos'
    )
    servicios = models.ManyToManyField(Servicio, related_name='dptos')  # Esta línea agrega la relación muchos a muchos con los servicios.
    equipamiento = models.ManyToManyField(Equipamiento, related_name='dptos')  # Agrega esta línea para la relación con equipamiento.

    class Meta:
        db_table = 'dpto'
        
#aca se guardaran las imagenes EN BLOB ORACLE
#class DptoImagen(models.Model):
#    departamento = models.ForeignKey(Dpto, on_delete=models.CASCADE, related_name='imagenes')
#    imagen = models.BinaryField()
#    
#    class Meta:
#        db_table = 'DptoImagen'
        
class DptoImagen(models.Model):
    departamento = models.ForeignKey(Dpto, on_delete=models.CASCADE, related_name='imagenes')
    imagen = models.ImageField(upload_to='dpto_imagenes/', null  = True)
    class Meta:
        db_table = 'DptoImagen'
    
class Direc(models.Model):
    id_direc = models.AutoField(primary_key=True)
    calle = models.CharField(max_length=50)
    numero = models.CharField(max_length=50)
    ndpto  = models.CharField(max_length=6)
    ciudad = models.CharField(max_length=25)
    region = models.CharField(max_length=25)
    pais = models.CharField(max_length=25)
    estado = models.CharField(max_length=20, default='activo')
    class Meta:
        db_table = 'direc'

      

class Mantencion(models.Model):
    id_mantencion = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=250)
    fecha_programada = models.DateField()
    estado = models.CharField(max_length=20, default='activo')
    dpto = models.ForeignKey(
        'dpto',
        on_delete=models.CASCADE,
        null=True,
        related_name='mantenciones'
    )
    class Meta:
        db_table = 'mantencion'

class ReporteGanancias(models.Model):
    id_reporte = models.AutoField(primary_key=True)
    fecha_generacion = models.DateField()
    tipo = models.CharField(max_length=50)
    ingresos = models.IntegerField()
    gastos = models.IntegerField()
    ganancias = models.IntegerField()
    estado = models.CharField(max_length=20, default='activo')
    dpto = models.ForeignKey(
        'dpto',
        on_delete=models.CASCADE,
        null=True,
        related_name='reportes'
    )
    class Meta:
        db_table = 'reporteganancias'

class Tour(models.Model):
    id_tour = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=25, unique=True)
    descripcion = models.CharField(max_length=100)
    duracion = models.IntegerField()
    fecha = models.DateField()  
    hora = models.TimeField()
    valor = models.IntegerField()
    estado = models.CharField(max_length=20, default='activo')
    customUser = models.ForeignKey(
        'customUser',
        on_delete=models.CASCADE,
        null=True,
        related_name='tours'
    )
    class Meta:
        db_table = 'tour'

class Traslado(models.Model):
    id_traslado = models.AutoField(primary_key=True)
    origen = models.CharField(max_length=25)
    destino = models.CharField(max_length=25)
    valor = models.IntegerField()
    fecha = models.DateField()  
    hora = models.TimeField()
    estado = models.CharField(max_length=20, default='activo')
    customUser = models.ForeignKey(
        'customUser',
        on_delete=models.CASCADE,
        null=True,
        related_name='traslados'
    )
    class Meta:
        db_table = 'traslado'
