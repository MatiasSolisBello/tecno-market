from django.shortcuts import render, redirect, get_object_or_404
from .models import ImageProduct, Products
from .forms import ContactForm, ProductsForm, CustomUserCreationForm
from .models import Contact
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import permission_required
from django.contrib.auth import authenticate, login
from django.http import Http404
from django.views.generic.edit import CreateView, UpdateView
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

class HomeView(View):
    def get(self, request):
        products = Products.objects.all()
        context = {'products':products}
        return render(request, 'app/home.html', context)

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
            text = f'{type_msg} enviada correctamente'
            messages.success(request, text)
        else:
            data["form"] = form
        return render(request, self.template_name, data)


class CreateProductsView(CreateView):
    model = Products
    form_class = ProductsForm
    template_name = 'app/products/form.html'
    
    def get(self, request):
        form = self.form_class()
        ctx = {'form': form }
        return render(request, self.template_name, ctx)
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST, files=request.FILES)
        
        images = request.FILES.getlist('image')

        if form.is_valid():
            product = form.save()
            for image in images:
                ImageProduct.objects.create(image=image, product=product)
               
            messages.success(request, "Agregado correctamente")
            return redirect('list')
        else:
            
            ctx = {'form': form }
            return render(request, self.template_name, ctx)
        

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

class UpdateProduct(UpdateView):
    model = Products
    form_class = ProductsForm
    template_name = 'app/products/form.html'
    
    def get(self, request, id):
        product = get_object_or_404(self.model, id=id)
        form = self.form_class(instance=product)
        ctx = {'form': form, 'instance': product}
        return render(request, self.template_name, ctx)
    
    def post(self, request, id):
        product = get_object_or_404(self.model, id=id)
        form = self.form_class(data=request.POST, instance=product, files=request.FILES)
        
        
        images = request.FILES.getlist('image')

        if form.is_valid():
            product = form.save()
            for image in images:
                ImageProduct.objects.create(image=image, product=product)
            
            messages.success(request, "Modificado correctamente")
            return redirect('list')
        
        ctx = {'form': form }
        return render(request, self.template_name, ctx)
    

@permission_required('app.delete_producto')
def delete(request, id):
    producto = get_object_or_404(Products, id=id)
    producto.delete()
    image = ImageProduct.objects.filter(product=producto)
    print('DELETE img: ', image)
    messages.warning(request, "Eliminado  correctamente")
    return redirect(to="list")


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