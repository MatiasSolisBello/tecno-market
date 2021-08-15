from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto
from .forms import ContactoForm, ProductoForm
from django.contrib import messages

# Create your views here.
def home(request):
    productos = Producto.objects.all()
    data = {
        'productos': productos
    }
    return render(request, 'app/home.html', data)

def contacto(request):
    data = {
        'form': ContactoForm()
    }

    if request.method == 'POST':
        formulario = ContactoForm(data = request.POST)
        if formulario.is_valid():
            formulario.save()
            data["mensaje"] = "Formulario recibido!!"
        else:
            data["form"] = formulario
    return render(request, 'app/contacto.html', data)

def agregar(request):
    data = {
        'form': ProductoForm()
    }
    if request.method == 'POST':
        formulario = ProductoForm(data = request.POST, files = request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Agregado correctamente")
            return redirect(to="listar")
        else:
            data["form"] = formulario

    return render(request, 'app/producto/agregar.html', data)

def listar(request):
    productos =Producto.objects.all()
    data = {
        'productos': productos
    }
    return render(request, 'app/producto/listar.html', data)

def modificar(request, id):
    producto = get_object_or_404(Producto, id=id)
    data = {
        'form': ProductoForm(instance=producto)
    }
    if request.method == 'POST':
        formulario = ProductoForm(data = request.POST, instance=producto, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Modificado correctamente")
            return redirect(to="listar")
        data["form"] = formulario
    return render(request, 'app/producto/modificar.html', data)

def eliminar(request, id):
    producto = get_object_or_404(Producto, id=id)
    producto.delete()
    messages.warning(request, "Eliminado  correctamente")
    return redirect(to="listar")
