from django import forms
from .models import Brand, Contact, ImageProduct, Products, Comment, Checkout
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column, Div, Layout, Row, Submit, HTML, Field
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

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
    """ image = forms.ImageField(required=False,
                             validators=[MaxSizeFileValidator(max_file_size=2)],
                             label="Imagen de producto",
                             widget=forms.ClearableFileInput(attrs={'multiple': True})
                            ) """

    # nombre con minimo de caracteres
    name = forms.CharField(min_length=3, max_length=50, label="Nombre")

    #precio con min. y max. de valor
    price = forms.IntegerField(min_value=1, max_value=1500000, label="Precio")

    # fecha
    fabrication_date = forms.DateField(widget=DateInput(), label="Fecha de fabricación")

    class Meta:
        model = Products
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-parsley'
        self.helper.include_media = False
        
        # Layout base
        layout = [
            Div(
                Row(
                    Column('name', css_class='col-md-4'),
                    Column('price', css_class='col-md-3'),
                    Column(
                        Div(
                            'brand',
                            HTML("""
                                <button type="button" class="btn btn-sm btn-outline-success ms-2"
                                    data-bs-toggle="modal" data-bs-target="#brandModal">
                                    +
                                </button>
                            """),
                            css_class="d-flex align-items-center"
                        ),
                        css_class='col-md-2'
                    ),
                    Column('fabrication_date', css_class='col-md-3')
                ),
                Row(
                    Column('description', css_class='col-md-12'),
                    Column('is_new', css_class='col-md-2'),
                ),
            )
        ]
        
        # Si estamos editando (producto existente)
        if self.instance and self.instance.pk:
            images = ImageProduct.objects.filter(product=self.instance.pk)
            if images.exists():
                images_html = "".join([
                    f"""
                    <div class='col-md-3 text-center mb-3'>
                        <img src='{img.image.url}' class='img-fluid rounded border' style='max-height:150px;'>
                        <div class='form-check mt-2'>
                            <input type='checkbox' name='delete_images' value='{img.id}' class='form-check-input'>
                            <label class='form-check-label'>Eliminar</label>
                        </div>
                    </div>
                    """ for img in images
                ])
            else:
                images_html = "<p class='text-muted'>No hay imágenes asociadas a este producto.</p>"

            layout.append(
                HTML(f"""
                    <hr>
                    <h5 class="mt-4">Imágenes actuales</h5>
                    <div class='row'>{images_html}</div>
                """)
            )

        # Campo de nuevas imágenes
        layout.append(
            HTML("""
                <div class="mt-3">
                    <label class="form-label fw-bold">Agregar nuevas imágenes</label>
                    <input type="file" name="image" multiple class="form-control">
                </div>
            """)
        )

        # Botón de envío
        layout.append(
            Row(
                Submit('submit', "Guardar", css_class='btn btn-success btn-lg float-end'),
                css_class="d-flex justify-content-end mt-4"
            )
        )

        self.helper.layout = Layout(*layout)


class ImageProductForm(forms.ModelForm):
    class Meta:
        model = ImageProduct
        fields = ['image']

class CustomUserCreationForm(UserCreationForm):

    #personalizar formulario de registro

    #condatos exiistentes
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password1", "password2"]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['product', 'name', 'title', 'text', 'rating']
        widgets = {
            # Limita a 1-5 en el formulario
            'rating': forms.HiddenInput(attrs={
                'min': 1, 'max': 5, 'readonly': True, 'required': True
            }),
            'product': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        product = kwargs.pop('product', None)
        request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

        if request.user.is_authenticated:
            full_name = f'{request.user.first_name} {request.user.last_name}'
            self.fields['name'].initial = full_name
            self.fields['name'].widget.attrs['readonly'] = True

        if product:
            self.fields['product'].initial = product

        self.helper = FormHelper()
        self.helper.form_class = 'form-parsley'
        self.helper.include_media = False
        self.helper.layout = Layout(
            Div(
                Row(
                    Column('name', css_class='col-md-4'),
                    Column('title', css_class='col-md-4'),
                    #Column('rating', css_class='col-md-4'),
                    Field('product'),
                    Field('rating'),
                    css_class="d-flex justify-content-center"
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


class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ['name']


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Checkout
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-parsley'
        self.helper.include_media = False
        self.helper.layout = Layout(
            Div(
                Row(
                    Column('email', css_class='col-md-4'),
                    Column('phone', css_class='col-md-4'),
                    Field('created_at'),
                ),
                Row(
                    Column('region', css_class='col-md-4'),
                    Column('province', css_class='col-md-4'),
                    Column('commune', css_class='col-md-4'),
                ),
                Row(
                    Column('name', css_class='col-md-3'),
                    Column('address', css_class='col-md-3'),
                    Column('reference', css_class='col-md-3'),
                    Column('total_price', css_class='col-md-3'),
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

