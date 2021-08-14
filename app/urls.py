from django.urls import path
from .views import home, contacto, agregar, listar

urlpatterns = [
    path('', home, name="home"),
    path('contacto/', contacto, name="contacto"),
    path('agregar/', agregar, name="agregar"),
    path('listar/', listar, name="listar"),

]
