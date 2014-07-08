from django.contrib.auth import authenticate, login, logout, get_user_model
from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.exceptions import PermissionDenied

from snotes20.serializers import NUserSerializer
from snotes20.models import NUser, NUserSocial, NUserSocialType


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
        if pk == "me":
            if not request.user.is_authenticated():
                raise PermissionDenied()

            data = NUserSerializer(request.user).data
            data['password'] = None
            return Response(data)
        else:
            user = get_object_or_404(NUser, username=pk)
            data = NUserSerializer(user).data

            return Response({
                'username': data['username'],
                'role': 'admin' if data['is_staff'] else 'user',
                'bio': data['bio'],
                'color': data['color'],
                'date_joined': data['date_joined'],
                'date_login': data['date_login'],
                'socials': data['socials'],
            })

    def partial_update(self, request, pk=None):
        user = request.user
        if pk != "me" or not user.is_authenticated():
            raise PermissionDenied()

        pwok = ('password' in request.DATA and user.check_password(request.DATA['password']))

        # Change password
        if 'newpassword' in request.DATA:
            if not pwok:
                raise PermissionDenied()
            else:
                newpw = request.DATA['newpassword']
                user.set_password(newpw)
                user.save()

                auth_user = authenticate(username=user.username, password=newpw)
                login(request, auth_user)

                return Response(status=status.HTTP_202_ACCEPTED)

        # Change email
        if 'email' in request.DATA and not pwok:
            raise PermissionDenied()

        # Change color or bio
        if 'password' in request.DATA:
            del request.DATA['password']

        serialized = NUserSerializer(user, data=request.DATA, partial=True)

        if serialized.is_valid():
            serialized.save()
            return Response(status=status.HTTP_202_ACCEPTED)
        else:
            return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)
