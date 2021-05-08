from rest_framework import serializers
from rest_framework.serializers import Serializer, CharField, IntegerField, ModelSerializer, EmailField, ValidationError, BooleanField
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from .models import *


class UserSerializer(Serializer):
    id = IntegerField(read_only=True)
    username = CharField(max_length=150)
    first_name = CharField(max_length=150)
    last_name = CharField(max_length=150)
   # clientprofile = BooleanField(default=True)


class RegisterSerializer(ModelSerializer):
    email = EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = CharField(write_only=True, required=True,
                         validators=[validate_password])
    password2 = CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2',
                  'email', 'first_name', 'last_name', 'clientprofile')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'clientprofile': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise ValidationError(
                {"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            clientprofile=validated_data['clientprofile']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class CatalogoSerializer(ModelSerializer):
    class Meta:
        model = Catalogo
        fields = ('id', 'fecha_creacion', 'admin_creador')


class CarritoSerializer(ModelSerializer):
    class Meta:
        model = Carrito
        fields = ('id', 'usuario_id', 'item_compras')


class ItemCompraSerializer(ModelSerializer):
    class Meta:
        model = ItemCompra
        fields = ('id', 'imagenUrl', 'visibilidad', 'catalogo')


class ItemCompraCarritoSerializer(ModelSerializer):
    class Meta:
        model = ItemCompraCarrito
        fields = ('item_compra_id', 'cantidad')


class CarritoDisplaySerializer(serializers.ModelSerializer):
    item_compras = serializers.SerializerMethodField()

    class Meta:
        model = Carrito
        fields = ('id', 'usuario_id', 'item_compras')

    def get_item_compras(self, carrito_instance):
        query_datas = ItemCompraCarrito.objects.filter(carrito=carrito_instance)
        return [ItemCompraCarritoSerializer(itemCompra).data for itemCompra in query_datas]


class ProductoSerializer(ModelSerializer):
    class Meta:
        model = Producto
        fields = ('id', 'nombre', 'precio')


class ClientSerializer(ModelSerializer):
    class Meta:
        model = ClientProfile
        fields = ('user', 'active', 'name')


class RegisterClientSerializer(ModelSerializer):

   # clientprofile = ClientSerializer(read_only=True)

    email = EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = CharField(write_only=True, required=True,
                         validators=[validate_password])
    password2 = CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2',
                  'email', 'first_name', 'last_name', 'clientprofile')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'clientprofile': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise ValidationError(
                {"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            clientprofile=validated_data['clientprofile']
        )

        user.set_password(validated_data['password'])

        user.save()

        return user


class ItemCompraSerializer1(ModelSerializer):
    class Meta:
        model = ItemCompra
        fields = ('id', 'imagenUrl', 'visibilidad')
