from django.contrib import admin
from .models import Brand, ImageProduct, Products, Contact, Comment
from .forms import ProductsForm

#-------------------------------------------------
# Validaciones aplicables en admin de django
#-------------------------------------------------
class ImageProductAdmin(admin.TabularInline):
    model = ImageProduct

class ProductsAdmin(admin.ModelAdmin):
    form = ProductsForm
    inlines = [
        ImageProductAdmin
    ]

# Register your models here.
admin.site.register(Brand)
admin.site.register(Products, ProductsAdmin)
admin.site.register(Contact)
admin.site.register(Comment)