from django import forms
from .models import Contact, ImageProduct, Products, Comment
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column, Div, Layout, Row, Submit
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .validators import MaxSizeFileValidator

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
                             label="Imagen de producto",
                             widget=forms.ClearableFileInput(attrs={'multiple': True})
                            )

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
        if self.instance.pk:
            images = ImageProduct.objects.filter(product=self.instance.pk)
            self.fields['image'].initial= images
        self.helper.include_media = False
        self.helper.layout = Layout(
            Div(
                Row(
                    Column('name', css_class='col-md-4'),
                    Column('price', css_class='col-md-3'),
                    Column('brand', css_class='col-md-2'),
                    Column('fabrication_date', css_class='col-md-3')
                ),
                Row(
                    Column('description', css_class='col-md-12'),
                ),
                Row(
                    Column('image', css_class='col-md-6'),
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
        
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'title', 'text', 'rating']
        widgets = {
            # Limita a 1-5 en el formulario
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-parsley'
        self.helper.include_media = False
        self.helper.layout = Layout(
            Div(
                Row(
                    Column('name', css_class='col-md-4'),
                    Column('title', css_class='col-md-4'),
                    Column('rating', css_class='col-md-4'),
                ),
                Row(
                    Column('text', css_class='col-md-12'),
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