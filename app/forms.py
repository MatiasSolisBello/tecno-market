from django import forms
from .models import Contacto, Producto

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
