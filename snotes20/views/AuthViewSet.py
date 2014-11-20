from datetime import datetime

from django.contrib.auth import authenticate, login, logout

from rest_framework.response import Response
from rest_framework import viewsets, status

import snotes20.models as models

class AuthViewSet(viewsets.ViewSet):
    permission_classes = ()

    def list(self, request):
        if request.user.is_authenticated() or (request.user is models.NUser and request.user.is_authenticated_raw()):
            return Response(data={'user': {'username': request.user.username, 'migrated': request.user.migrated}}, status=200)
        else:
            return Response(status=401)

    def create(self, request):
        username = request.DATA['username']
        password = request.DATA['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                user.date_login = datetime.now()
                user.save()
                return Response(data={'migrated': user.migrated}, status=200)
            else:
                return Response(status=401)
        else:
            return Response(status=401)

    def destroy(self, request, pk=None):
        logout(request)
        return Response(status=200)
