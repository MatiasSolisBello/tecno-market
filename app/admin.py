from django.contrib import admin
from .models import Brand, Products, Contact
from .forms import ProductsForm

#-------------------------------------------------
# Validaciones aplicables en admin de django
#-------------------------------------------------
class ProductsAdmin(admin.ModelAdmin):
    form = ProductsForm

# Register your models here.
admin.site.register(Brand)
admin.site.register(Products)
admin.site.register(Contact)