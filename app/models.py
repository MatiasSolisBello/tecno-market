from django.db import models

# Create your models here.
class Marca(models.Model):
    nombre = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    precio = models.IntegerField()
    descripcion = models.TextField()
    nuevo = models.BooleanField()
    marca = models.ForeignKey(Marca, on_delete=models.PROTECT)
    fecha_fabricacion = models.DateField()

    def __str__(self):
        return self.nombre