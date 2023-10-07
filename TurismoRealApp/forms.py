from django import forms
from django.core import validators
from .models import *
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
import re
from django.forms.widgets import CheckboxSelectMultiple
#eleccion de regiones

region_choices = [
    ('Arica y Parinacota', 'Arica y Parinacota'),
    ('Tarapacá', 'Tarapacá'),
    ('Antofagasta', 'Antofagasta'),
    ('Atacama', 'Atacama'),
    ('Coquimbo', 'Coquimbo'),
    ('Valparaíso', 'Valparaíso'),
    ('Metropolitana de Santiago', 'Metropolitana de Santiago'),
    ('Libertador General Bernardo O\'Higgins', 'Libertador General Bernardo O\'Higgins'),
    ('Maule', 'Maule'),
    ('Ñuble', 'Ñuble'),
    ('Biobío', 'Biobío'),
    ('La Araucanía', 'La Araucanía'),
    ('Los Ríos', 'Los Ríos'),
    ('Los Lagos', 'Los Lagos'),
    ('Aysén del General Carlos Ibáñez del Campo', 'Aysén del General Carlos Ibáñez del Campo'),
    ('Magallanes y de la Antártica Chilena', 'Magallanes y de la Antártica Chilena'),
]

#eleccion de paises
country_choices = [
    ('Chile', 'Chile'),
]
#lista de ciudades
city_choices = [
    ('Santiago', 'Santiago'),
    ('Valparaíso', 'Valparaíso'),
    ('Viña del Mar', 'Viña del Mar'),
    ('Pucón', 'Pucón'),
    ('San Pedro de Atacama', 'San Pedro de Atacama'),
    ('Puerto Varas', 'Puerto Varas'),
    ('Valdivia', 'Valdivia'),
    ('La Serena', 'La Serena'),
    ('Arica', 'Arica'),
    ('Iquique', 'Iquique'),
    ('Antofagasta', 'Antofagasta'),
    ('Calama', 'Calama'),
    ('Ovalle', 'Ovalle'),
    ('Coquimbo', 'Coquimbo'),
    ('La Serena', 'La Serena'),
    ('Valdivia', 'Valdivia'),
    ('Castro', 'Castro'),
    ('Ancud', 'Ancud'),
    ('Puerto Montt', 'Puerto Montt'),
    ('Frutillar', 'Frutillar'),
    ('Punta Arenas', 'Punta Arenas'),
    ('Puerto Natales', 'Puerto Natales'),
    ('Osorno', 'Osorno'),
    ('Villarrica', 'Villarrica'),
    ('Puerto Octay', 'Puerto Octay'),
    ('Vichuquén', 'Vichuquén'),
    ('Lican Ray', 'Lican Ray'),
    ('Horcon', 'Horcon'),
    ('Maitencillo', 'Maitencillo'),
    ('Papudo', 'Papudo'),
    ('Valparaíso', 'Valparaíso'),
    ('Zapallar', 'Zapallar'),
    ('Arica', 'Arica'),
    ('Valdivia', 'Valdivia'),
    ('Iquique', 'Iquique'),
    ('Rancagua', 'Rancagua'),
    ('Los Ángeles', 'Los Ángeles'),
    ('Chillán', 'Chillán'),
    ('Talca', 'Talca'),
    ('Curicó', 'Curicó'),
    ('Pichilemu', 'Pichilemu'),
    ('Cauquenes', 'Cauquenes'),
    ('Talcahuano', 'Talcahuano'),
    ('Concepción', 'Concepción'),
    ('Los Ángeles', 'Los Ángeles'),
    ('Valdivia', 'Valdivia'),
    ('Puerto Montt', 'Puerto Montt'),
    ('Frutillar', 'Frutillar'),
    ('Osorno', 'Osorno'),
    ('Puerto Octay', 'Puerto Octay'),
    ('Puerto Varas', 'Puerto Varas'),
    ('Puerto Natales', 'Puerto Natales'),
    ('Coyhaique', 'Coyhaique'),
    ('Futaleufú', 'Futaleufú'),
    ('Puerto Aysén', 'Puerto Aysén'),
    ('Cochrane', 'Cochrane'),
    ('Punta Arenas', 'Punta Arenas'),
    ('Porvenir', 'Porvenir'),
]

#formulario departamentos
class formCrearDepartamentos(forms.Form):
    nombre = forms.CharField(
        label='Nombre',
        widget=forms.TextInput(attrs={'style': 'width: 100%;','placeholder': 'Ingrese nombre del departamento'}),
        validators=[
            validators.MinLengthValidator(3, 'Error, el mínimo de caracteres es 3'),
            validators.RegexValidator(r'^[A-Za-z0-9ñÑáéíóúÁÉÍÓÚ\s]*$', 'Error, caracteres no permitidos'),
        ]
    )
    descripcion = forms.CharField(
        label='Descripción',
        widget=forms.TextInput(attrs={'style': 'width: 100%;','placeholder': 'Ingrese descripción del departamento'}),
        validators=[
            validators.MinLengthValidator(3, 'Error, el mínimo de caracteres es 3'),
            validators.RegexValidator(r'^[A-Za-z0-9ñÑáéíóúÁÉÍÓÚ\s]*$', 'Error, caracteres no permitidos'),
        ]
    )
    tarifa_diaria = forms.IntegerField(
        widget=forms.NumberInput(attrs={'style': 'width: 100%;', 'placeholder': 'Ingrese valor de la tarifa'}),
        validators=[
            validators.MaxValueValidator(limit_value=99999999999, message='El valor de la tarifa no debe superar 99,999,999,999'),
        ]
    )
    # Campos de dirección
    calle = forms.CharField(
        label='Calle',
        widget=forms.TextInput(attrs={'style': 'width: 100%;','placeholder': 'Ingrese calle'}),
    ) 
    numero = forms.CharField(
        label='Numero',
        widget=forms.TextInput(attrs={'style': 'width: 100%;','placeholder': 'Ingrese numero'}),
    ) 
    ndpto = forms.CharField(
        label='Numero de dpto',
        max_length=6,
        widget=forms.TextInput(attrs={'style': 'width: 100%;','placeholder': 'Ingrese numero de dpto'}),
    )  
    region = forms.ChoiceField(
        label='Región',
        choices=region_choices,
        widget=forms.Select(attrs={'style': 'width: 100%;', 'placeholder': 'Seleccione la región'}),
    )    
    ciudad = forms.ChoiceField(
        label='Ciudad',
        choices=city_choices,
        widget=forms.Select(attrs={'style': 'width: 100%;','placeholder': 'Seleccione la ciudad'}),
    )
    pais = forms.ChoiceField(
        label='País',
        choices=country_choices,
        widget=forms.Select(attrs={'style': 'width: 100%;','placeholder': 'Seleccione el país'}),
    )
    
    # Campos para las imágenes
    imagen_1 = forms.ImageField(
        label='Imagen 1',
        required=False,
        widget=forms.ClearableFileInput(attrs={'style': 'width: 100%;'}),
    )
    imagen_2 = forms.ImageField(
        label='Imagen 2',
        required=False,
        widget=forms.ClearableFileInput(attrs={'style': 'width: 100%;'}),
    )
    imagen_3 = forms.ImageField(
        label='Imagen 3',
        required=False,
        widget=forms.ClearableFileInput(attrs={'style': 'width: 100%;'}),
    )
    imagen_4 = forms.ImageField(
        label='Imagen 4',
        required=False,
        widget=forms.ClearableFileInput(attrs={'style': 'width: 100%;'}),
    )
    imagen_5 = forms.ImageField(
        label='Imagen 5',
        required=False,
        widget=forms.ClearableFileInput(attrs={'style': 'width: 100%;'}),
    )
    imagen_6 = forms.ImageField(
        label='Imagen 6',
        required=False,
        widget=forms.ClearableFileInput(attrs={'style': 'width: 100%;'}),
    )
    imagen_7 = forms.ImageField(
        label='Imagen 7',
        required=False,
        widget=forms.ClearableFileInput(attrs={'style': 'width: 100%;'}),
    )
    servicios = forms.ModelMultipleChoiceField(
        label='Servicios',
        required=False,
        queryset=Servicio.objects.filter(estado='activo'), 
        widget=forms.CheckboxSelectMultiple,
        to_field_name='nombre' #solo muestre los nombres en los checkbox
         
    )

##--  
#agrega formato al rut
class RutInput(forms.TextInput):
    def format_value(self, value):
        if not value:
            return value

        # Elimina todos los caracteres no numéricos
        cleaned_value = ''.join(filter(str.isdigit, str(value)))

        # Formatea el RUT con puntos y guión
        formatted_value = '-'.join([cleaned_value[:-1], cleaned_value[-1]])

        return formatted_value
#form crear usuario
class CustomUserCreationForm(UserCreationForm):
    rut = forms.CharField(
        max_length=20,
        widget=RutInput(attrs={'placeholder': 'Ingrese su RUT'}),
    )
    telefono = forms.CharField(
        label='Telefono',
        widget=forms.TextInput(attrs={'placeholder': 'Ingrese su telefono'}),
        validators=[
            validators.MinLengthValidator(3, 'Error, el mínimo de caracteres es 3'),
            validators.RegexValidator(r'^[0-9+]*$', 'Error, caracteres no permitidos'),
        ]
    )
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('rut', 'telefono','email')
    def clean_rut(self):
        rut = self.cleaned_data['rut']
        # Validar el RUT chileno
        if not es_rut_chileno_valido(rut):
            raise forms.ValidationError('El RUT no es válido.')
        return rut
    
#valida rut chileno
def es_rut_chileno_valido(rut):
    # Expresión regular para validar RUT chileno
    rut_pattern = re.compile(r'^\d{1,2}\.\d{3}\.\d{3}[-][0-9kK]{1}$')
    if not rut_pattern.match(rut):
        return False

    rut_digits, verificador = rut.split('-')
    rut_digits = rut_digits.replace('.', '')

    suma = 0
    multiplicador = 2
    for d in reversed(rut_digits):
        suma += int(d) * multiplicador
        multiplicador += 1
        if multiplicador == 8:
            multiplicador = 2

    resto = suma % 11
    digito_verificador = 11 - resto
    if digito_verificador == 11:
        digito_verificador = 0
    elif digito_verificador == 10:
        digito_verificador = 'K'

    return str(digito_verificador).upper() == verificador.upper()    

#crear tour
class TourCreationForm(forms.ModelForm):
    valor = forms.IntegerField(
        widget=forms.NumberInput(attrs={'style': 'width: 100%;', 'placeholder': 'Ingrese el valor'}),
        validators=[
            validators.MaxValueValidator(limit_value=99999999999, message='El valor no debe superar 99,999,999,999'),
        ]
    )
    duracion = forms.IntegerField(
        widget=forms.NumberInput(attrs={'style': 'width: 100%;', 'placeholder': 'Ingrese la duración en minutos'}),
        validators=[
            validators.MaxValueValidator(limit_value=999, message='La duración no debe superar 99,999,999,999 minutos'),
        ]
    )
    fecha = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'style': 'width: 100%;', 'placeholder': 'Seleccione la fecha'}),
    )
    hora = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time', 'style': 'width: 100%;', 'placeholder': 'Seleccione la hora'}),
    )

    class Meta:
        model = Tour
        fields = ['nombre', 'descripcion', 'duracion', 'valor','fecha','hora']
    
#crear traslado
class TrasladoCreationForm(forms.ModelForm):
    valor = forms.IntegerField(
        widget=forms.NumberInput(attrs={'style': 'width: 100%;', 'placeholder': 'Ingrese el valor'}),
        validators=[
            validators.MaxValueValidator(limit_value=99999999999, message='El valor no debe superar 99,999,999,999'),
        ]
    )
    fecha = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'style': 'width: 100%;', 'placeholder': 'Seleccione la fecha'}),
    )
    hora = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time', 'style': 'width: 100%;', 'placeholder': 'Seleccione la hora'}),
    )
    class Meta:
        model = Traslado
        fields = ['origen', 'destino', 'valor','fecha','hora']
        
#form creacion de servicio
class ServicioForm(forms.ModelForm):
    class Meta:
        model = Servicio
        fields = ['nombre']
        
class EquipamientoForm(forms.ModelForm):
    class Meta:
        model = Equipamiento
        fields = ['objeto', 'valor']  # Especifica los campos que deseas en el formulario
#para buscar ciudades o nombre en detalles dpto
class BuscarCiudadForm(forms.Form):
       busqueda = forms.CharField(label='Buscar', required=False, widget=forms.TextInput(attrs={'placeholder': 'Ingrese ciudad o nombre'}))

