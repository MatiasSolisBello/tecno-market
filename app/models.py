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