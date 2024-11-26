from django.conf import settings
from django.db import models
from django.utils.timesince import timesince
from djchoices import ChoiceItem, DjangoChoices
from django.utils.translation import gettext as _

#-------------------------------------------------
#           Create your models here.
#-------------------------------------------------
class Brand(models.Model):
    name = models.CharField(max_length=200,  verbose_name=_("Nombre de marca"))

    def __str__(self): return self.name

class Products(models.Model):
    name = models.CharField(max_length=200, verbose_name=_("Nombre de Producto"))
    price = models.IntegerField(verbose_name=_("Precio"))
    description = models.TextField(verbose_name=("Descripción"))
    is_new = models.BooleanField(verbose_name=("Nuevo"))
    brand = models.ForeignKey(
        Brand, verbose_name=("Marca"), on_delete=models.PROTECT)
    fabrication_date = models.DateField(verbose_name=_("Fecha de Fabricación"))
    #image = models.ImageField(
    #    verbose_name=_("Imagen"), upload_to="products")

    def __str__(self): return self.name

class ImageProduct(models.Model):
    image = models.ImageField(upload_to="products")
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name="images")

class Comment(models.Model):
    """
    Comentarios
    """
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=200, verbose_name=_("Tu nombre"), blank=True, null=True)

    title = models.CharField(max_length=50, verbose_name=("Titulo de comentario"))
    text = models.TextField(verbose_name=("Comentario"))

    rating = models.PositiveSmallIntegerField(default=0)  # Campo de calificación de 1 a 5
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.title

    def days_since(self):
        delta = timesince(self.timestamp)
        return delta.split(",")[0]


class Region(models.Model):
    """
    Region
    """

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=80, verbose_name=_("Descripción"))
    ordinal = models.CharField(max_length=4, verbose_name=_("Ordinal"))

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = _("Región")
        verbose_name_plural = _("Regiones")

        ordering = ('ordinal',)

class Province(models.Model):
    """
    provincia
    """

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=80)
    region = models.ForeignKey("Region", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = _("Provincia")
        verbose_name_plural = _("Provincias")

class Commune(models.Model):
    """
    comunas
    """

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, verbose_name=_("Descripción"))
    code = models.IntegerField(unique=True, null=True, verbose_name=("Código"))
    province = models.ForeignKey(
        "Province", on_delete=models.CASCADE, verbose_name=_("Provincia")
    )
    region = models.ForeignKey(
        "Region", on_delete=models.CASCADE, null=True, verbose_name=_("Región")
    )

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = _("Comuna")
        verbose_name_plural = _("Comunas")

        ordering = ('province__region__ordinal', 'name')


class Checkout(models.Model):
    #Contacto
    email = models.EmailField(verbose_name=("Correo de contacto"))
    phone = models.IntegerField(null=True, verbose_name=("Número de telefono"))

    # Entrega
    region = models.ForeignKey(
        'Region',
        null=True,
        on_delete=models.CASCADE,
        verbose_name=_("Región")
    )
    province = models.ForeignKey(
        "Province", on_delete=models.CASCADE, verbose_name=_("Provincia")
    )
    commune = models.ForeignKey(
        'Commune',
        null=True,
        on_delete=models.CASCADE,
        verbose_name=_("Comuna")
    )
    name = models.CharField(max_length=100, verbose_name=("Nombre Completo"))
    address = models.CharField(max_length=100, verbose_name=("Dirección"))
    reference = models.CharField(max_length=100, verbose_name=("Referencia"))
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pedido de {self.name}"

    class Meta:
        verbose_name = _("Región")
        verbose_name_plural = _("Regiones")

class CheckoutItem(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE,
                                related_name='product')
    checkout = models.ForeignKey(Checkout, on_delete=models.CASCADE,
                                related_name='checkout')
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product}"

# Las consultas solo acepta estas opciones
class OptionsEnquiry(DjangoChoices):
    CONSULTA = ChoiceItem(1, "Consulta")
    RECLAMO = ChoiceItem(2, "Reclamo")
    SUGERENCIA = ChoiceItem(2, "Sugerencia")
    FELICITACIONES = ChoiceItem(2, "Felicitaciones")

class Contact(models.Model):
    name = models.CharField(max_length=50, verbose_name=("Nombre Completo"))
    email = models.EmailField(verbose_name=("Correo"))
    type_enquiry = models.IntegerField(
        choices=OptionsEnquiry.choices,
        verbose_name=("Tipo de consulta")
    )
    message = models.TextField(verbose_name=("Mensaje"))
    notice = models.BooleanField(verbose_name=("Aviso"))

    def __str__(self):
        return self.name
