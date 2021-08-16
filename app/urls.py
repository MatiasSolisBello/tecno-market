from django.urls import path
from .views import home, contacto, agregar, listar, modificar, eliminar, registro

urlpatterns = [
    # url / vista /alias

    path('', home, name="home"),
    path('contacto/', contacto, name="contacto"),
    path('agregar/', agregar, name="agregar"),
    path('listar/', listar, name="listar"),
    path('modificar/<id>/', modificar, name="modificar"),
    path('eliminar/<id>/', eliminar, name="eliminar"),

    path('registro/', registro, name="registro"),


]
