from django.contrib.auth import authenticate, login, logout, get_user_model
from django.shortcuts import get_object_or_404
from django.db import transaction

from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import action

from snotes20.serializers import NUserRegisterSerializer, NUserSerializer
from snotes20.models import NUser


class UserViewSet(viewsets.ViewSet):
    permission_classes = ()

    def create(self, request):
        serialized = NUserRegisterSerializer(data=request.DATA)

        if serialized.is_valid():
            user = get_user_model().objects.create_user(
                email=serialized.init_data['email'],
                username=serialized.init_data['username'],
                password=serialized.init_data['password']
            )
            token = user.add_email_token(user.email)
            user.email_user_activation('de', token.token)
            user.is_active = False
            user.save()
            return Response(None, status=status.HTTP_201_CREATED)
        else:
            return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['POST'])
    def activate(self, request, pk=None):
        try:
            token = request.DATA['token']
            user = NUser.objects.get(username=pk)
            token_obj = user.check_email_token(token)
            user.apply_email_token(token_obj)
            return Response(status=status.HTTP_202_ACCEPTED)
        except:
            raise PermissionDenied()

    @action(methods=['POST'])
    def request_pw_reset(self, request, pk=None):
        try:
            user = NUser.objects.get(username=pk)
            user.set_pw_reset_token()
            user.email_pw_reset('de')
        except:
            pass
        return Response(status=status.HTTP_200_OK)

    @action(methods=['POST'])
    def pw_reset(self, request, pk=None):
        try:
            token = request.DATA['token']
            password = request.DATA['password']
            user = NUser.objects.get(username=pk)
            if user.check_pw_reset_token(token):
                user.apply_pw_reset_token(password)
                return Response(status=status.HTTP_200_OK)
        except:
            pass
        raise PermissionDenied()

    @action(methods=['POST'])
    def upgrade(self, request, pk=None):
        if not request.user.is_authenticated_raw() or request.user.migrated:
            raise PermissionDenied()

        if 'password' not in request.DATA:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        password = request.DATA['password']
        user = request.user
        user.migrate(password, request=request)

        return Response(status=status.HTTP_200_OK)

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
        if 'action' not in request.QUERY_PARAMS:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        action = request.QUERY_PARAMS['action']
        data = request.DATA

        pwok = ('password' in request.DATA and user.check_password(request.DATA['password']))

        if action == 'colorbio':
            data = {'color': data['color'], 'bio': data['bio'] }
        elif action == 'socials':
            data = {'socials': data['socials']}
        elif action == 'email':
            if not pwok: raise PermissionDenied()

            email = data['email']

            with transaction.atomic():
                token = user.add_email_token(email).token
                user.email_new_mail_confirmation('de', token, email)
                user.save()

            return Response(status=status.HTTP_202_ACCEPTED)
        elif action == 'password':
            if not pwok: raise PermissionDenied()
            user.set_password_keep_session(request, data['newpassword'])
            return Response(status=status.HTTP_202_ACCEPTED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serialized = NUserSerializer(user, data=data, partial=True)

        if serialized.is_valid():
            serialized.object.full_clean()
            serialized.save()
            return Response(status=status.HTTP_202_ACCEPTED)
        else:
            return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)
