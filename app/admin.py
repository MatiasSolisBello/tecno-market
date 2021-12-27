from django.contrib import admin
from .models import Marca, Producto, Contacto, ImagenProducto
from .forms import ProductoForm

#validaciones aplicables en admin de django
class ImagenProductoAdmin(admin.TabularInline):
    model = ImagenProducto

class ProductoAdmin(admin.ModelAdmin):
    form = ProductoForm
    inlines = [
        ImagenProductoAdmin
    ]


# Register your models here.
admin.site.register(Marca)
admin.site.register(Producto, ProductoAdmin)
admin.site.register(Contacto)