from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


# Create your models here.
class Catalogo(models.Model):
    fecha_creacion = models.DateField(verbose_name='Fecha de creacion')
    admin_creador = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name_plural = "Catalogos"


class ItemCompra(models.Model):
    imagenUrl = models.CharField(max_length=500)
    visibilidad = models.BooleanField()
    catalogo = models.ForeignKey(to=Catalogo, on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name_plural = "Items"


class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.FloatField()
    itemId = models.ForeignKey(to=ItemCompra, on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name_plural = "Productos"


class Carrito(models.Model):
    usuario_id = models.OneToOneField(User, on_delete=models.CASCADE)
    item_compras = models.ManyToManyField(ItemCompra, through='ItemCompraCarrito')

    class Meta:
        verbose_name_plural = "carritos"


class ItemCompraCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.PROTECT)
    item_compra = models.ForeignKey(ItemCompra, on_delete=models.PROTECT)
    cantidad = models.IntegerField()

    class Meta:
        verbose_name_plural = "ItemsCompraCarrito"


class ClientProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    name = models.CharField(max_length=64)

    def __str__(self):
        return f'Profile for user {self.name}'
