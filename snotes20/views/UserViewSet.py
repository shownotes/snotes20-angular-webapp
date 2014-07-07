from django.contrib.auth import authenticate, login, logout, get_user_model

from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.exceptions import PermissionDenied

from snotes20.serializers import NUserSerializer


class UserViewSet(viewsets.ViewSet):
    permission_classes = ()

    def create(self, request):
        serialized = NUserSerializer(data=request.DATA)

        if serialized.is_valid():
            user = get_user_model().objects.create_user(
                email=serialized.init_data['email'],
                username=serialized.init_data['username'],
                password=serialized.init_data['password']
            )
            user.email_user_activation('en', 'asdasd')
            return Response(None, status=status.HTTP_201_CREATED)
        else:
            return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        if pk != "me" or not request.user.is_authenticated():
            raise PermissionDenied()

        data = NUserSerializer(request.user).data
        data['password'] = None
        return Response(data)
