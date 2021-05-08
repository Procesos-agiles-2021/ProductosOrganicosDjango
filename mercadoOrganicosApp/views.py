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
def signin(request):
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
def signout(request):
    do_signout(request, user=request.user)
    return redirect('/')


@csrf_exempt
def login_view(request):
    return render(request, "login.html")


@csrf_exempt
def signup(request):
    if request.method == 'POST':
        newUser = User(
            username=request.POST.get('username'),
            password=request.POST.get('password'),
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone'))
        newUser.save()
    return HttpResponse(serializers.serialize("json", [newUser]))


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
def carrito_list_create(request, userPk):
    try:
        if request.method == 'GET':
            carrito = Carrito.objects.filter(usuario_id=userPk)
            serializer = CarritoSerializer(carrito, many=True)
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


@api_view(["GET", "POST", "PUT"])
def itemcarrito_list_create(request, userPk):
    try:
        if request.method == 'GET':
            carrito = Carrito.objects.filter(usuario_id=userPk)
            serializer = CarritoDisplaySerializer(carrito, many=True)
            return Response(serializer.data)
        elif request.method == 'POST':
            carrito = Carrito.objects.filter(usuario_id=userPk).first()
            itemCompra_id = request.data['item_compras'][0]['itemCompra_id']
            itemCompra = ItemCompra.objects.filter(id=itemCompra_id).first()
            cantidad = request.data['item_compras'][0]['cantidad']
            itemCompraCarrito = ItemCompraCarrito.objects.filter(item_compra=itemCompra, carrito=carrito)

            if not itemCompraCarrito.exists():
                itemCompraNuevo = ItemCompraCarrito(carrito=carrito, item_compra=itemCompra, cantidad=cantidad)
                itemCompraNuevo.save()
                return Response(status=status.HTTP_200_OK)
            else:
                item = itemCompraCarrito.first()
                cant = int(cantidad) + item.cantidad
                itemCompraCarrito.update(cantidad=cant)
                return Response(status=status.HTTP_200_OK)
                return Response(status=status.HTTP_400_BAD_REQUEST)
    except Carrito.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["PUT", "DELETE"])
def itemcarrito_update_delete(request, userPk, itemPk):
    try:
        if request.method == 'DELETE':
            carrito = Carrito.objects.filter(usuario_id=userPk).first()
            itemCompra = ItemCompra.objects.filter(id=itemPk).first()
            itemCompraCarrito = ItemCompraCarrito.objects.filter(item_compra=itemCompra, carrito=carrito)

            if itemCompraCarrito.exists():
                itemCompraCarrito.delete()
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        elif  request.method == 'PUT':
            carrito = Carrito.objects.filter(usuario_id=userPk).first()
            itemCompra = ItemCompra.objects.filter(id=itemPk).first()
            itemCompraCarrito = ItemCompraCarrito.objects.filter(item_compra=itemCompra, carrito=carrito)

            if itemCompraCarrito.exists():
                itemCompraCarrito.update(cantidad=request.data['cantidad'])
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
    except Carrito.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def producto_get(request, catPk, itemPk):
    if request.method == 'GET':
        producto = Producto.objects.filter(itemId=itemPk)
        serializer = ProductoSerializer(producto, many=True)
        return Response(serializer.data)


@api_view(["GET"])
def items_get(request, catPk):
    if request.method == 'GET':
        item = ItemCompra.objects.filter(catalogo=catPk)
        serializer = ItemCompraSerializer1(item, many=True)
        return Response(serializer.data)


class RegisterClientView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterClientSerializer
