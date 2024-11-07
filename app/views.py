from django.shortcuts import render, redirect, get_object_or_404
from .models import ImageProduct, Products
from .forms import ContactForm, ProductsForm, CustomUserCreationForm, ImageProductFormSet
from .models import Contact
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import authenticate, login
from django.http import Http404
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views import View
from django.urls.base import reverse_lazy
from rest_framework import viewsets
from .serializers import ProductsSerializer

class ProductsViewset(viewsets.ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductsSerializer

    # Filtrar por variable de nombre => localhost:8000/api/products/?name=televisor
    def get_queryset(self):
        products = Products.objects.all() 
        name = self.request.GET.get('name')
        if name:
            products = products.filter(name__contains=name)
        return products

#para mostrar solo si necesita login, sin importar permiso
# @login_required

# --------------------------
# Create your views here.
#---------------------------
#def home(request):
#    productos = Producto.objects.all()
#    data = {
#        'productos': productos
#    }
#    return render(request, 'app/home.html', data)


class HomeView(View):
    def get(self, request):
        products = Products.objects.all()
        context = {'products':products}
        return render(request, 'app/home.html', context)
    

#def detalles(request, id):
#    productos = get_object_or_404(Producto, id=id)
#    data = {
#        'productos': productos
#    }
#    return render(request, 'app/producto/detalles.html', data)

class DetallesView(View):
    template_name = 'app/products/details.html'
    
    def get(self, request, id):
        products = get_object_or_404(Products, id = id)
        images = ImageProduct.objects.filter(product_id=id)
        context = {
            'products':products, 
            'images': images
        }
        return render(request, self.template_name, context)
    


#def contacto(request):
#    data = {
#        'form': ContactoForm()
#    }
#
#    if request.method == 'POST':
#        formulario = ContactoForm(data = request.POST)
#        if formulario.is_valid():
#            formulario.save()
#            data["mensaje"] = "Formulario recibido!!"
#        else:
#            data["form"] = formulario
#    return render(request, 'app/contacto.html', data)


class ContactView(View):
    model = Contact
    form_class = ContactForm
    template_name = 'app/contact.html'
    
    def get(self, request):
        form = self.form_class()
        ctx = {'form': form}
        return render(request, self.template_name, ctx)
        
    def post(self, request):
        data = {
            'form': self.form_class()
        }
        form = self.form_class(data = request.POST)
        if form.is_valid():
            form.save()
            type_msg = form.cleaned_data
            print('  -> ', type_msg)
            text = f'{type_msg} enviada correctamente'
            messages.success(request, text)
        else:
            data["form"] = form
        return render(request, self.template_name, data)



#@permission_required('app.add_producto')
#def agregar(request):
#    data = {
#        'form': ProductoForm()
#    }
#    if request.method == 'POST':
#        formulario = ProductoForm(data = request.POST, files = request.FILES)
#        if formulario.is_valid():
#            formulario.save()
#            messages.success(request, "Agregado correctamente")
#            return redirect(to="listar")
#        else:
#            data["form"] = formulario
#   return render(request, 'app/producto/agregar.html', data)

#@permission_required('app.add_producto')
class CreateProductsView(CreateView):
    model = Products
    form_class = ProductsForm
    template_name = 'app/products/form.html'
    
    def get(self, request):
        form = self.form_class()
        formset = ImageProductFormSet()
        ctx = {'form': form, 'formset': formset}
        print('ctx: ', ctx)
        return render(request, self.template_name, ctx)
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST, files=request.FILES)
        formset = ImageProductFormSet(request.POST, request.FILES)
        print('request.POST: ', request.POST)

        if form.is_valid() and formset.is_valid():
            product = form.save()
            for image_form in formset:
                image = image_form.save(commit=False)
                image.product = product
                image.save()
            messages.success(request, "Agregado correctamente")
            return redirect('list')
        else:
            print('Form errors:', form.errors)
            print('Formset errors:', formset.errors)
            ctx = {'form': form, 'formset': formset}
            return render(request, self.template_name, ctx)
        


#@permission_required('app.view_producto')
#def listar(request):
#    productos =Producto.objects.all()
#
    #Si page no existe en url del navegador, devuelve la pagina 1
#    page = request.GET.get('page', 1) 

#    try:
        #5 productos x pagina, y los muestra segun valor de "page"
#        paginator = Paginator(productos, 5) 
#        productos = paginator.page(page)
#    except:
#        raise Http404
#    data = {
#        'entity': productos, #entity para uso de paginador
#        'paginator': paginator
#    }
#    return render(request, 'app/producto/listar.html', data)

#@permission_required('app.view_producto')
class ListProductsView(View):
    model = Products
    template_name = 'app/products/list.html'
    
    def get(self, request):
        products = self.model.objects.all()
        page = request.GET.get('page', 1)
        try:
            #5 products x pagina, y los muestra segun valor de "page"
            paginator = Paginator(products, 5) 
            products = paginator.page(page)
        except:
            raise Http404
        data = {
            'entity': products, #entity para uso de paginador
            'paginator': paginator
        }
        
        return render(request, self.template_name, data)


#@permission_required('app.change_producto')
#def modificar(request, id):
#    producto = get_object_or_404(Products, id=id)
#    data = {
#        'form': ProductsForm(instance=producto)
#    }
#    if request.method == 'POST':
#        formulario = ProductsForm(data = request.POST, instance=producto, files=request.FILES)
#        if formulario.is_valid():
#            formulario.save()
#            messages.success(request, "Modificado correctamente")
#            return redirect(to="list")
#        data["form"] = formulario
#    return render(request, 'app/products/modificar.html', data)


class UpdateProduct(UpdateView):
    model = Products
    form_class = ProductsForm
    template_name = 'app/products/form.html'
    
    def get(self, request, id):
        product = get_object_or_404(self.model, id=id)
        form = self.form_class(instance=product)
        formset = ImageProductFormSet(instance=product)
        ctx = {'form': form, 'formset': formset, 'instance': product}
        return render(request, self.template_name, ctx)
    
    def post(self, request, id):
        product = get_object_or_404(self.model, id=id)
        form = self.form_class(data=request.POST, instance=product, files=request.FILES)
        formset = ImageProductFormSet(request.POST, request.FILES, instance=product)

        print('form: ', form.is_valid())
        print('formset: ', formset.is_valid())

        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, "Modificado correctamente")
            return redirect('list')
        
        ctx = {'form': form, 'formset': formset}
        return render(request, self.template_name, ctx)

    
    

@permission_required('app.delete_producto')
def delete(request, id):
    producto = get_object_or_404(Products, id=id)
    producto.delete()
    messages.warning(request, "Eliminado  correctamente")
    return redirect(to="list")

#def registro(request):
#    data = {
#        'form': CustomUserCreationForm()
#    }
#    if request.method == 'POST':
#        formulario = CustomUserCreationForm(data = request.POST)
#        if formulario.is_valid():
#            formulario.save()

            #loguear al usuario terminado el registro
#            user = authenticate(username=formulario.cleaned_data["username"], password=formulario.cleaned_data["password1"])
#            login(request, user)
#            messages.success(request, "Registro Correcto")
#            return redirect(to="home")

#        data["form"] = formulario
#    return render(request, 'registration/singup.html', data)

class SingUpView(View):
    model = Products
    form_class = CustomUserCreationForm
    template_name = 'registration/singup.html'
    
    def get(self, request):
        data = {'form': self.form_class}
        return render(request, self.template_name, data)
    
    def post(self, request):
        data = {'form': self.form_class}
        form = self.form_class(data = request.POST)
        if form.is_valid():
            form.save()

            #loguear al usuario terminado el registro
            user = authenticate(
                username = form.cleaned_data["username"], 
                password = form.cleaned_data["password1"]
            )
            login(request, user)
            messages.success(request, "Registro Correcto")
            return redirect(to="home")
        data["form"] = form
        return render(request, 'registration/singup.html', data)