from django import forms
from .models import Contact, Products
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Column, Div, Field, Layout, Row, Submit
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .validators import MaxSizeFileValidator
from django.forms import ValidationError

#
from functools import partial
DateInput = partial(forms.DateInput, {'class': 'datepicker'})



class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-parsley'
        self.helper.include_media = False
        self.helper.layout = Layout(
            Div(
                Row(
                    Column('name', css_class='col-md-4'),
                    Column('email', css_class='col-md-4'),
                    Column('type_enquiry', css_class='col-md-4'),
                ),
                Row(
                    Column('message', css_class='col-md-12'),
                ),
                Row(
                    Column('notice', css_class='col-md-2'),
                ),
                Row(
                    Submit(
                        'submit', "Enviar",
                        css_class='btn btn-success btn-lg float-right'
                    ),
                    css_class="d-flex justify-content-end"
                )
            ),
        )


class ProductsForm(forms.ModelForm):

    # imagen no requerido y con peso maximo
    image = forms.ImageField(required=False, 
                             validators=[MaxSizeFileValidator(max_file_size=2)],
                             label="Imagen de producto")

    # nombre con minimo de caracteres
    name = forms.CharField(min_length=3, max_length=50, label="Nombre")

    #precio con min. y max. de valor
    price = forms.IntegerField(min_value=1, max_value=1500000, label="Precio")

    # fecha
    fabrication_date = forms.DateField(widget=DateInput(), label="Fecha de fabricación")

    # nombre no se puede repetir
    #def clean_nombre(self):
    #    nombre = self.cleaned_data["nombre"]
    #    existe = Producto.objects.filter(nombre__iexact=nombre).exists()
    #   if existe:
    #        raise ValidationError("El nombre ya existe")
    #   return nombre



    class Meta:
        model = Products
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-parsley'
        print(self.instance.id)
        self.helper.include_media = False
        self.helper.layout = Layout(
            Div(
                Row(
                    Column('name', css_class='col-md-4'),
                    Column('price', css_class='col-md-4'),
                    Column('brand', css_class='col-md-4')
                ),
                Row(
                    Column('description', css_class='col-md-12'),
                ),
                Row(
                    Column('fabrication_date', css_class='col-md-4'),
                    Column('image', css_class='col-md-6'),
                ),
                Row(
                    Column('is_new', css_class='col-md-2'),
                ),
                Row(
                    Submit(
                        'submit', "Enviar",
                        css_class='btn btn-success btn-lg float-right'
                    ),
                    css_class="d-flex justify-content-end"
                )
            )
        )
        
        
class CustomUserCreationForm(UserCreationForm):
    
    #personalizar formulario de registro

    #condatos exiistentes
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password1", "password2"]