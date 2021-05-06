from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token


def signin(request, username, password):
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        user.save()
        token = Token.objects.get_or_create(user=user)[0]
        return user, token.key
    else:
        raise Exception('Error on credentials')


def signout(request, user):
    token = Token.objects.get(user=user)
    logout(request)
    token.delete()
