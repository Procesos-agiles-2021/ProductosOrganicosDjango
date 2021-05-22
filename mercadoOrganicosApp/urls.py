"""mercadoOrganico URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('', redirect_to_home, name="Home"),
    path('admin/', admin.site.urls),
    path('signin', sign_in, name='Sign In'),
    path('signout', sign_out, name='Sign Out'),
    path('login/', login_view, name='login'),
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('catalogo/', catalogos_list_post, name='catalogos_list_post'),
    path('catalogo/<int:catPk>/itemproducto/<int:itemPk>', producto_get, name='producto_get_by_itemId'),
    path('catalogo/<int:cat_pk>/items', items_get, name='items_get_by_catalogoId'),
    path('itemproducto/<int:itemPk>', productoCarrito_get, name='productoCarrito_get_by_itemId'),
    path('user/<int:userPk>/catalogo/<int:pk>',
         catalogos_update_delete, name='catalogos_update_delete'),
    path('registerClient/', RegisterClientView.as_view(), name='client_register'),
    path('carrito/<int:userPk>', shopping_cart_list_create, name='shopping_cart_list_create'),
    path('itemcarrito/<int:user_pk>', shopping_cart_item_list_create, name='shopping_cart_item_list_create'),
    path('itemcarrito/<int:user_pk>/itemcompra/<int:item_pk>', shopping_cart_item_update_delete,
         name='shopping_cart_item_update_delete'),
]
