import json
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Brand, ImageProduct, OptionsEnquiry, Products, Contact, Comment
from .cart import Cart
from .forms import (BrandForm, CommentForm, CheckoutForm, ContactForm, 
                    ImageProductForm, ProductsForm, CustomUserCreationForm)
from django.contrib import messages
from django.views.generic import TemplateView
from django.core.paginator import Paginator
from django.contrib.auth.decorators import permission_required
from django.contrib.auth import authenticate, login
from django.db.models import Count, Avg
from django.http import Http404
from django.http import JsonResponse
from django.views.generic.edit import CreateView, UpdateView
from django.views import View
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
    model = Comment
    template_name = 'app/products/details.html'
    form_class = CommentForm

    def get(self, request, id):
        product = get_object_or_404(Products, id = id)
        images = ImageProduct.objects.filter(product_id=id)
        images_text = f'{images.count()} imagenes'
        comments = Comment.objects.filter(product_id=id)

        form = self.form_class(product=product, request=request)

        # Calcular el promedio de calificación
        avg_rating = comments.aggregate(Avg('rating'))['rating__avg'] or 0
        
        # Calcular la cantidad de cada calificación (1 a 5)
        ratings_count = comments.values('rating').annotate(count=Count('rating'))
        rating_distribution = {i: 0 for i in range(1, 6)}
        total_comments = comments.count()

        for item in ratings_count:
            rating_distribution[item['rating']] = item['count']

        # Calcular el porcentaje para cada calificación
        rating_percentage = {
            k: (v / total_comments * 100) if total_comments > 0 else 0
            for k, v in rating_distribution.items()
        }

        rating_percentage = {k: f"{v:.1f}%" for k, v in rating_percentage.items()}

        context = {
            'product':product,
            'images': images,
            'images_text': images_text,
            'comments': comments,
            'form': form,
            'range': range(5),
            'avg_rating': round(avg_rating),
            'rating_percentage': rating_percentage
        }
        return render(request, self.template_name, context)

    def post(self, request, id):
        data = {
            'form': self.form_class(request=request)
        }
        form = self.form_class(data=request.POST, request=request)
        if form.is_valid():
            form.save()
            messages.success(request, "Comentario enviado correctamente")
        else:
            data["form"] = form
        return redirect(request.META['HTTP_REFERER'])


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
            type_msg = OptionsEnquiry(form.cleaned_data["type_enquiry"])
            text = f'{type_msg.label} enviada correctamente'
            messages.success(request, text)
        else:
            data["form"] = form
        return render(request, self.template_name, data)


class CreateProductsView(LoginRequiredMixin, CreateView):
    model = Products
    form_class = ProductsForm
    template_name = 'app/products/form.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = kwargs.get('form', self.form_class())
        context['brand_form'] = BrandForm()
        return context

    def get(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        context = self.get_context_data(form=form)
        return self.render_to_response(context)

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


class ListProductsView(LoginRequiredMixin, View):
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

class UpdateProduct(LoginRequiredMixin, UpdateView):
    model = Products
    form_class = ProductsForm
    template_name = 'app/products/form.html'

    def get(self, request, id):
        product = get_object_or_404(self.model, id=id)
        form = self.form_class(instance=product)
        ctx = {
            'form': form, 
            'instance': product,
            'images': product.images.all(),
            'image_form': ImageProductForm()
        }
        return render(request, self.template_name, ctx)
    
    def post(self, request, id):
        product = get_object_or_404(self.model, id=id)
        form = self.form_class(data=request.POST, instance=product, files=request.FILES)
        images = request.FILES.getlist('image')
        delete_images = request.POST.getlist('delete_images')

        if form.is_valid():
            product = form.save()
            
            # eliminar imágenes seleccionadas
            if delete_images:
                ImageProduct.objects.filter(id__in=delete_images, 
                                            product=product).delete()
                
            # agregar nuevas imágenes
            for image in images:
                ImageProduct.objects.create(image=image, product=product)
            messages.success(request, "Modificado correctamente")
            return redirect('list')

        ctx = {'form': form, 'images': product.images.all()  }
        return render(request, self.template_name, ctx)


@permission_required('app.delete_producto')
def delete(request, id):
    product = get_object_or_404(Products, id=id)
    product.delete()
    image = ImageProduct.objects.filter(product=product)
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

class BrandCreateView(LoginRequiredMixin, CreateView):
    model = Brand
    form_class = BrandForm

    def form_valid(self, form):
        brand = form.save()
        return JsonResponse({'id': brand.id, 'name': brand.name}, status=201)

    def form_invalid(self, form):
        return JsonResponse({'errors': form.errors}, status=400)



class CheckoutView(View):
    form_class = CheckoutForm
    template_name = 'app/products/checkout.html'

    def get(self, request):
        form = self.form_class()
        ctx = {'form': form}
        return render(request, self.template_name, ctx)



class AddToCartView(View):
    def post(self, request, product_id):
        product = get_object_or_404(Products, id=product_id)
        quantity = int(request.POST.get('quantity', 1))
        cart = Cart(request)

        cart.add(product, quantity)

        #request.session['quantity_cart'] += 1
        return JsonResponse({'success': True, 'cart': cart.cart})


class CartDetailView(TemplateView):
    """
    Carrito
    """
    template_name = 'app/products/cart.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = Cart(self.request)
        context['cart'] = cart.items()
        context['total_price'] = cart.get_total_price()
        return context

    def post(self, request):
        cart = request.session.get('cart', {})
        #print('-----------------')
        #print(type(cart))

        #for i in cart:
        #    print(i)

        return redirect('checkout')

class ClearCartView(View):
    def post(self, request):
        cart = Cart(request)
        cart.clear()
        return redirect('cart')

class RemoveFromCartView(View):
    def post(self, request, product_id):
        product = get_object_or_404(Products, id=product_id)
        cart = Cart(request)
        cart.remove(product)

        # Actualizar quantity_cart
        #request.session['cart']

        return JsonResponse({
            'success': True,
            'cart': cart.cart,
            'cart_count': len(cart)
        })


class UpdateCartView(View):
    def post(self, request, product_id):
        product = get_object_or_404(Products, id=product_id)
        quantity = int(request.POST.get('quantity', 1))
        cart = Cart(request)
        cart.add(product, quantity - cart.cart.get(str(product_id), {}).get('quantity', 0))

        return JsonResponse({
            'success': True,
            'cart': cart.cart,
            'cart_count': len(cart),
        })


""" class UpdateCartView(View):
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        quantity = int(request.POST.get('quantity', 1))
        cart = Cart(request)
        cart.add(product, quantity - cart.cart.get(str(product_id), {}).get('quantity', 0))

        return JsonResponse({
            'success': True,
            'cart': cart.cart,
            'cart_count': len(cart),
        }) """

class UpdateCartNumbersView(View):
    """
    """
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        product_id = data.get('product_id')
        quantity = data.get('quantity')
        self.request.session['quantity_cart'] = quantity

        if not product_id or not quantity:
            return JsonResponse({'success': False}, status=400)

        # Obtener el carrito de la sesión
        cart = request.session.get('cart', {})

        if str(product_id) in cart:
            cart[str(product_id)]['quantity'] = quantity
            cart[str(product_id)]['total'] = cart[str(product_id)]['price'] * quantity

        # Calcular el precio total
        total_price = sum(item['total'] for item in cart.values())

        # Guardar los cambios en la sesión
        request.session['cart'] = cart

        return JsonResponse({
            'success': True,
            'item_total': cart[str(product_id)]['total'],
            'total_price': total_price,
            'quantity': quantity
        })
