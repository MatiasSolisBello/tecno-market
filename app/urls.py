
import debug_toolbar
from django.conf import settings
from django.urls import path, include
from .views import (AddToCartView, BrandCreateView, CartDetailView, HomeView, ContactView, CreateProductsView, ClearCartView,
                    DetallesView, ListProductsView, UpdateProduct, RemoveFromCartView,
                    delete, SingUpView, ProductsViewset, CheckoutView, 
                    CartDetailView, UpdateCartView, UpdateCartNumbersView)
from rest_framework import routers

router =routers.DefaultRouter()
router.register('products', ProductsViewset)

urlpatterns = [
    # url / vista /alias

    path('', HomeView.as_view(), name="home"),
    path('contact/', ContactView.as_view(), name="contact"),
    path('create/', CreateProductsView.as_view(), name="create"),
    path('list/', ListProductsView.as_view(), name="list"),
    path('details/<int:id>/', DetallesView.as_view(), name="details"),
    path('update/<int:id>/', UpdateProduct.as_view(), name="update"),
    path('delete/<int:id>/', delete, name="delete"),
    path('cart/remove/<int:product_id>/', RemoveFromCartView.as_view(), name='remove_from_cart'),

    path('update-cart/', UpdateCartNumbersView.as_view(), name='update-cart'),
    path('create-brand/', BrandCreateView.as_view(), name='brand-create'),
    path('singup/', SingUpView.as_view(), name="singup"),
    
    #path('cart/', CartView.as_view(), name="cart"),
    path('checkout/', CheckoutView.as_view(), name="checkout"),
    path('cart/add/<int:product_id>/', AddToCartView.as_view(), name='add_to_cart'),
    path('cart/clear/', ClearCartView.as_view(), name='clear_cart'),
    path('cart/', CartDetailView.as_view(), name='cart'),
    path('api/', include(router.urls)),
    path('cart/update/<int:product_id>/', UpdateCartView.as_view(), name='update_cart'),
]

if settings.DEBUG:
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]