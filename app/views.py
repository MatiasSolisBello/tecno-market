from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto
from .forms import ContactoForm, ProductoForm, CustomUserCreationForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import Http404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, permission_required
from rest_framework import viewsets
from .serializers import ProductoSerializer

class ProductoViewset(viewsets.ModelViewSet):
    queryset =Producto.objects.all()  #puedo reemplazar all() por filter()
    serializer_class = ProductoSerializer

    # Filtrar por variable de nombre => localhost:8000/api/producto/?nombre=televisor
    def get_queryset(self):
        productos = Producto.objects.all() 
        nombre = self.request.GET.get('nombre')
        if nombre:
            productos = productos.filter(nombre__contains=nombre)
        return productos

#para mostrar solo si necesita login, sin importar permiso
# @login_required

# --------------------------
# Create your views here.
#---------------------------
def home(request):
    productos = Producto.objects.all()
    data = {
        'productos': productos
    }
    return render(request, 'app/home.html', data)

def detalles(request, id):
    productos = get_object_or_404(Producto, id=id)
    data = {
        'productos': productos
    }
    return render(request, 'app/producto/detalles.html', data)

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

@permission_required('app.add_producto')
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

@permission_required('app.view_producto')
def listar(request):
    productos =Producto.objects.all()

    #Si page no existe en url del navegador, devuelve la pagina 1
    page = request.GET.get('page', 1) 

    try:
        #5 productos x pagina, y los muestra segun valor de "page"
        paginator = Paginator(productos, 5) 
        productos = paginator.page(page)
    except:
        raise Http404
    data = {
        'entity': productos, #entity para uso de paginador
        'paginator': paginator
    }
    return render(request, 'app/producto/listar.html', data)

@permission_required('app.change_producto')
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

@permission_required('app.delete_producto')
def eliminar(request, id):
    producto = get_object_or_404(Producto, id=id)
    producto.delete()
    messages.warning(request, "Eliminado  correctamente")
    return redirect(to="listar")

def registro(request):
    data = {
        'form': CustomUserCreationForm()
    }
    if request.method == 'POST':
        formulario = CustomUserCreationForm(data = request.POST)
        if formulario.is_valid():
            formulario.save()

            #loguear al usuario terminado el registro
            user = authenticate(username=formulario.cleaned_data["username"], password=formulario.cleaned_data["password1"])
            login(request, user)
            messages.success(request, "Registro Correcto")
            return redirect(to="home")

        data["form"] = formulario
    return render(request, 'registration/registro.html', data)