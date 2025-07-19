from django.contrib import admin
from .models import Brand, ImageProduct, Products, Contact, Comment
from .forms import ProductsForm

#-------------------------------------------------
# Validaciones aplicables en admin de django
#-------------------------------------------------
class ImageProductInline(admin.TabularInline):
    model = ImageProduct
    extra = 1

class ProductsAdmin(admin.ModelAdmin):
    form = ProductsForm
    inlines = [
        ImageProductInline
    ]

# Register your models here.
admin.site.register(Brand)
admin.site.register(Products, ProductsAdmin)
admin.site.register(Contact)
admin.site.register(Comment)