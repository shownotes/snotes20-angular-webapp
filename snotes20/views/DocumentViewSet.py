from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly

import snotes20.serializers as serializers
import snotes20.models as models


class DocumentViewSet(viewsets.ViewSet):
#    permission_classes = (IsAuthenticatedOrReadOnly,)

    def create(self, request):
        serialized = serializers.DocumentSerializer(data=request.DATA)

        if serialized.is_valid():
            doc = serialized.data

            doc.creator = request.user

            if 'episode' not in serialized.init_data:
                raise PermissionDenied()

            serialized.save()

            return Response(None, status=status.HTTP_201_CREATED)
        else:
            return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        pass

    #def list(self, request):
    #    pass

    #def update(self, request, pk=None):
    #    pass

    #def partial_update(self, request, pk=None):
    #    pass

    #def destroy(self, request, pk=None):
    #    pass