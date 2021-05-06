from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import Catalogo, Producto, ItemCompra, ClientProfile

# Register your models here.


@admin.register(Catalogo)
class CatalogoAdmin(admin.ModelAdmin):
    list_display = ('fecha_creacion', 'admin_creador')


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'itemId')


@admin.register(ItemCompra)
class ItemCompraAdmin(admin.ModelAdmin):
    list_display = ('imagenUrl', 'visibilidad', 'catalogo')


@admin.register(ClientProfile)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['user', 'active', 'name']
