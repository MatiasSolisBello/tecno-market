from .models import Producto, Marca
from rest_framework import serializers

# Declarar serializadores ==> Convertir datos a JSON  
class MarcaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marca
        fields = '__all__'

class ProductoSerializer(serializers.ModelSerializer):

    # Mostrar nombre de la marca y no solo el id. Solo de lectura
    nombre_marca = serializers.CharField(read_only=True, source="marca.nombre")

    # Mostrar datos de marca en GET Producto
    marca = MarcaSerializer(read_only=True)

    # Mostrar solo el id
    marca_id = serializers.PrimaryKeyRelatedField(queryset = Marca.objects.all(), source="marca")

    # Validaciones para nombre => requerido y minimo de caracteres
    nombre = serializers.CharField(required=True, min_length=3)

    # Funcion para evitar ingreso de 2 nombres iguales
    def validate_nombre(self, value):
        existe = Producto.objets.filter(nombre__iexact = value).exists()
        if existe:
            raise serializers.ValidationError("Este producto ya existe")
        return value

    class Meta:
        model = Producto       #modelo a serializar
        fields = '__all__'     #serializa todo, puedes poner 

        #para excluir agrega exlude, pero elimina "fields"
        #exclude = ['nombre']

         