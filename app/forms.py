from django import forms
from .models import Contacto, Producto
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .validators import MaxSizeFileValidator
from django.forms import ValidationError



class ContactoForm(forms.ModelForm):
    class Meta:
        model = Contacto
        fields = '__all__'

class ProductoForm(forms.ModelForm):

    # imagen no requerido y con peso maximo
    imagen = forms.ImageField(required=False, validators=[MaxSizeFileValidator(max_file_size=2)])

    # nombre con minimo de caracteres
    nombre = forms.CharField(min_length=3, max_length=50)

    #precio con min. y max. de valor
    precio = forms.IntegerField(min_value=1, max_value=1500000)

    # fecha
    fecha_fabricacion = forms.DateField(required=True)

    # nombre no se puede repetir
    def clean_nombre(self):
        nombre = self.cleaned_data["nombre"]
        existe = Producto.objects.filter(nombre__iexact=nombre).exists()

        if existe:
            raise ValidationError("El nombre ya existe")
        return nombre



    class Meta:
        model = Producto
        fields = '__all__'
    
        #Transforma la fecha a widget para mejor visualizacion
        widgets= {
            "fecha_fabricacion": forms.SelectDateWidget()
        }
        
class CustomUserCreationForm(UserCreationForm):
    
    #personalizar formulario de registro

    #condatos exiistentes
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password1", "password2"]