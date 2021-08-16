from django import forms
from .models import Contacto, Producto
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class ContactoForm(forms.ModelForm):
    class Meta:
        model = Contacto
        fields = '__all__'

class ProductoForm(forms.ModelForm):
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