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
from django.conf.urls import url

urlpatterns = [
    path('', redirect_to_home, name="Home"),
    path('admin/', admin.site.urls),
    path('signin', signin, name='Sign In'),
    path('signout', signout, name='Sign Out'),
    path('login/', login_view, name='login'),
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('catalogo/', catalogos_list_post, name='catalogos_list_post'),
    path('catalogo/<int:catPk>/itemproducto/<int:itemPk>', producto_get, name='producto_get_by_itemId'),
    path('catalogo/<int:catPk>/items', items_get, name='items_get_by_catalogoId'),
    # path('user/<int:userPk>/catalogo/', catalogos_list_post, name='Catalogos'),
    path('user/<int:userPk>/catalogo/<int:pk>',
         catalogos_update_delete, name='catalogos_update_delete'),
    path('registerClient/', RegisterClientView.as_view(), name='client_register'),
    path('carrito/<int:userPk>', carrito_list_create, name='carrito_list_create'),
    path('itemcarrito/<int:userPk>', itemcarrito_list_create, name='itemcarrito_list_create'),
    path('itemcarrito/<int:userPk>/itemcompra/<int:itemPk>', itemcarrito_update_delete, name='itemcarrito_update_delete'),
]
