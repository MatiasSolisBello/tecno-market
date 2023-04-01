from .models import Products, Brand
from rest_framework import serializers

# Declarar serializadores ==> Convertir datos a JSON  
class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'

class ProductsSerializer(serializers.ModelSerializer):

    # Mostrar nombre de la marca y no solo el id. Solo de lectura
    name_brand = serializers.CharField(read_only=True, source="brand.name")

    # Mostrar datos de marca en GET Producto
    brand = BrandSerializer(read_only=True)

    # Mostrar solo el id
    brand_id = serializers.PrimaryKeyRelatedField(
        queryset = Brand.objects.all(), source="brand"
    )

    # Validaciones para nombre => requerido y minimo de caracteres
    name = serializers.CharField(required=True, min_length=3)

    # Funcion para evitar ingreso de 2 nombres iguales
    def validate_name(self, value):
        exist = Products.objets.filter(name__iexact = value).exists()
        if exist:
            raise serializers.ValidationError("Este producto ya existe")
        return value

    class Meta:
        model = Products    #modelo a serializar
        fields = '__all__'     #serializa todo, puedes poner 

        #para excluir agrega exlude, pero elimina "fields"
        #exclude = ['name']

         