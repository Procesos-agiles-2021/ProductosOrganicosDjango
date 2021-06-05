from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, generics, serializers
from .logic import signin as do_signup, signout as do_signout
from .serializers import *
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


@api_view(["POST"])
def sign_in(request):
    username = request.data.get('username', '')
    password = request.data.get('password', None)
    try:
        user, token = do_signup(request, username, password)
        return Response({
            'token': token,
            'data': UserSerializer(user).data,
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_403_FORBIDDEN)


@api_view(["POST"])
def sign_out(request):
    do_signout(request, user=request.user)
    return Response(status=status.HTTP_200_OK)


@csrf_exempt
def login_view(request):
    return render(request, "login.html")


@csrf_exempt
def signup(request):
    if request.method == 'POST':
        new_user = User(
            username=request.POST.get('username'),
            password=request.POST.get('password'),
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone'))
        new_user.save()
    return HttpResponse(serializers.serialize("json", [new_user]))


def redirect_to_home(request):
    return redirect('/login')


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


@api_view(["GET", "POST"])
def catalogos_list_post(request):
    if request.method == 'GET':
        catalogos = Catalogo.objects.all()
        serializer = CatalogoSerializer(catalogos, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        print(request.data)
        serializer = CatalogoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.error, status=status.HTTP_404_NOT_FOUND)


@api_view(["PUT", "DELETE"])
def catalogos_update_delete(request, userPk, pk):
    try:
        catalogo = Catalogo.objects.get(pk=pk)
        if request.method == 'PUT':
            serializer = CatalogoSerializer(catalogo, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        elif request.method == 'DELETE':
            catalogo.delete()
            return Response(status=status.HTTP_200_OK)
    except Catalogo.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "POST"])
def shopping_cart_list_create(request, user_pk):
    try:
        if request.method == 'GET':
            shopping_cart = Carrito.objects.filter(usuario_id=user_pk)
            serializer = CarritoSerializer(shopping_cart, many=True)
            return Response(serializer.data)
        elif request.method == 'POST':
            serializer = CarritoSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
    except Carrito.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "POST"])
def shopping_cart_item_list_create(request, user_pk):
    try:
        if request.method == 'GET':
            shopping_cart = Carrito.objects.filter(usuario_id=user_pk)
            serializer = CarritoDisplaySerializer(shopping_cart, many=True)
            return Response(serializer.data)
        elif request.method == 'POST':
            shopping_item_id, quantity = get_creation_shopping_cart_item_params(request)
            shopping_cart_request = get_shopping_cart_request(user_pk, shopping_item_id)

            if not shopping_cart_request.shopping_cart_item.exists():
                create_shopping_cart_item(shopping_cart_request.shopping_cart, shopping_cart_request.purchase_item,
                                          quantity)
                return Response(status=status.HTTP_200_OK)
            else:
                update_item_quantity(shopping_cart_request.shopping_cart_item, quantity)
                return Response(status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def get_creation_shopping_cart_item_params(request):
    shopping_item_id = request.data['item_compras'][0]['itemCompra_id']
    quantity = request.data['item_compras'][0]['cantidad']
    return shopping_item_id, quantity


def get_shopping_cart_request(user_pk, shopping_item_id):
    shopping_cart = Carrito.objects.filter(usuario_id=user_pk).first()
    purchase_item = ItemCompra.objects.filter(id=shopping_item_id).first()
    shopping_cart_item = ItemCompraCarrito.objects.filter(item_compra=purchase_item, carrito=shopping_cart)
    return ShoppingCartRequest(shopping_cart_item, shopping_cart, purchase_item)


def create_shopping_cart_item(shopping_cart, purchase_item, quantity):
    new_shopping_cart_item = ItemCompraCarrito(carrito=shopping_cart, item_compra=purchase_item,
                                               cantidad=quantity)
    new_shopping_cart_item.save()


def update_item_quantity(shopping_cart_item, quantity):
    item = shopping_cart_item.first()
    cant = int(quantity) + item.cantidad
    shopping_cart_item.update(cantidad=cant)


@api_view(["PUT", "DELETE"])
def shopping_cart_item_update_delete(request, user_pk, item_pk):
    try:
        if request.method == 'DELETE':
            shopping_cart_item = get_shopping_cart_item(user_pk, item_pk)
            if shopping_cart_item.exists():
                shopping_cart_item.delete()
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        elif request.method == 'PUT':
            shopping_cart_item = get_shopping_cart_item(user_pk, item_pk)
            if shopping_cart_item.exists():
                shopping_cart_item.update(cantidad=request.data['cantidad'])
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
    except Carrito.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)


def get_shopping_cart_item(user_pk, item_pk):
    shopping_cart = Carrito.objects.filter(usuario_id=user_pk).first()
    purchase_item = ItemCompra.objects.filter(id=item_pk).first()
    shopping_cart_item = ItemCompraCarrito.objects.filter(item_compra=purchase_item, carrito=shopping_cart)
    return shopping_cart_item


@api_view(["GET"])
def producto_get(request, catPk, itemPk):
    if request.method == 'GET':
        producto = Producto.objects.filter(itemId=itemPk)
        if producto.exists():
            ofertas = Oferta.objects.filter(productoId=producto.values_list('id', flat=True).first())
            cantidadStock = 0
            for f in ofertas:
                cantidadStock += f.cantidadRestante
            producto.update(cantidad=cantidadStock)
        serializer = ProductoSerializer(producto, many=True)
        return Response(serializer.data)


@api_view(["GET"])
def productoCarrito_get(request, itemPk):
    if request.method == 'GET':
        producto = Producto.objects.filter(itemId=itemPk)
        serializer = ProductoSerializer(producto, many=True)
        return Response(serializer.data)


@api_view(["GET"])
def items_get(request, cat_pk):
    if request.method == 'GET':
        item = ItemCompra.objects.filter(catalogo=cat_pk)
        serializer = ItemCompraSerializer1(item, many=True)
        return Response(serializer.data)


@api_view(["GET"])
def producto_catalogo_remove(request, catPk, itemPk):
    print("llegó este id: " + str(itemPk))
    item = ItemCompra.objects.filter(catalogo=catPk, id=itemPk)
    if item.exists():
        item.update(visibilidad=False)
    serializer = ItemCompraSerializer1(item, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def producto_catalogo_add(request, catPk, itemPk):
    print("llegó este id: " + str(itemPk))
    item = ItemCompra.objects.filter(catalogo=catPk, id=itemPk)
    if item.exists():
        item.update(visibilidad=True)
    serializer = ItemCompraSerializer1(item, many=True)
    return Response(serializer.data)


class RegisterClientView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterClientSerializer


@api_view(["POST"])
def create_order(request):
    shopping_cart_id = request.data['carrito']
    try:
        shopping_cart = Carrito.objects.filter(usuario_id=shopping_cart_id)
        if shopping_cart.exists():
            serializer = OrdenSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
def get_order(request, user_pk):
    if request.method == 'GET':
        shopping_cart = Carrito.objects.filter(usuario_id=user_pk).first()
        orden_cart = Orden.objects.filter(carrito_id=shopping_cart)
        serializer = OrdenSerializer(orden_cart, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
def get_order_unit(request, orden_pk):
    if request.method == 'GET':
        orden_cart = Orden.objects.filter(id=orden_pk)
        serializer = OrdenSerializer(orden_cart, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
def decrease_inv(request, p_pk, cant):
    if request.method == 'GET':
        producto = Producto.objects.filter(id=p_pk)
        if producto.exists():
            ofertas = Oferta.objects.filter(productoId=producto.values_list('id', flat=True).first()).order_by('precioUnidad')
            cantidadStock = 0
            cantidadNueva = 0
            for f in ofertas:
                if cant > 0:
                    if cant <= f.cantidadRestante:
                        cantidadNueva = f.cantidadRestante - cant
                        cant = 0
                    else:
                        cantidadNueva = 0
                        cant -= f.cantidadRestante
                    f.cantidadRestante = cantidadNueva
                    f.save()
                cantidadStock += f.cantidadRestante
            producto.update(cantidad=cantidadStock)
        serializer = ProductoSerializer(producto, many=True)
        return Response(serializer.data)