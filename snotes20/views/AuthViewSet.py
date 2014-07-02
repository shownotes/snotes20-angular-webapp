from django.contrib.auth import authenticate, login, logout

from rest_framework.response import Response
from rest_framework import viewsets, status


class AuthViewSet(viewsets.ViewSet):
    permission_classes = ()

    def create(self, request):
        username = request.DATA['username']
        password = request.DATA['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return Response(status=200)
            else:
                return Response(status=401)
        else:
            return Response(status=401)

    def destroy(self, request, pk=None):
        logout(request)
        return Response(status=200)
