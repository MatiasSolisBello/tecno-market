from django.urls import path, include
from .views import (HomeView, ContactView, CreateProductsView, 
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
    path('singup/', SingUpView.as_view(), name="singup"),
    path('api/', include(router.urls)),


]
