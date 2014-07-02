from django.contrib.auth import authenticate, login, logout, get_user_model

from rest_framework.response import Response
from rest_framework import viewsets, status

from snotes20.serializers import UserSerializer


class UserViewSet(viewsets.ViewSet):
    permission_classes = ()

    def create(self, request):
        serialized = UserSerializer(data=request.DATA)

        if serialized.is_valid():
            get_user_model().objects.create_user(
                email=serialized.init_data['email'],
                username=serialized.init_data['username'],
                password=serialized.init_data['password']
            )
            return Response(None, status=status.HTTP_201_CREATED)
        else:
            return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)
