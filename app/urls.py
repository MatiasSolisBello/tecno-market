
import debug_toolbar
from django.conf import settings
from django.urls import path, include
from .views import (BrandCreateView, HomeView, ContactView, CreateProductsView, 
                    DetallesView, ListProductsView, UpdateProduct, 
                    delete, SingUpView, ProductsViewset)
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
    path('create-brand/', BrandCreateView.as_view(), name='brand-create'),
    path('singup/', SingUpView.as_view(), name="singup"),
    path('api/', include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]