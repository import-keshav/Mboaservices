from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from rest_framework import generics, status

from . import serializers as client_serializers
from . import models as client_models

from User import models as user_models


class GetClient(generics.ListAPIView):
    renderer_classes = [JSONRenderer]
    queryset = client_models.Client.objects.all()
    serializer_class = client_serializers.ClientGetSerializer


class UpdateClient(generics.UpdateAPIView):
    renderer_classes = [JSONRenderer]
    queryset = client_models.Client.objects.all()
    serializer_class = client_serializers.ClientUpdateSerializer


class CreateGetClientNotification(generics.ListCreateAPIView):
    renderer_classes = [JSONRenderer]
    serializer_class = client_serializers.ClientNotificationSerializer

    def get_queryset(self):
        client = client_models.Client.objects.filter(pk=self.kwargs['pk']).first()
        return client_models.ClientNotification.objects.filter(client=client)


class CreateGetClientCart(generics.ListCreateAPIView):
    renderer_classes = [JSONRenderer]

    def get_queryset(self):
        client = client_models.Client.objects.filter(pk=self.kwargs['pk']).first()
        return client_models.ClientCart.objects.filter(client=client)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return client_serializers.ClientCartGetSerializer
        return client_serializers.ClientCartPostSerializer


class UpdateClientCart(generics.UpdateAPIView):
    renderer_classes = [JSONRenderer]
    serializer_class = client_serializers.ClientCartUpdateSerializer
    queryset = client_models.ClientCart.objects.all()


class DeleteClientCart(generics.DestroyAPIView):
    renderer_classes = [JSONRenderer]
    serializer_class = client_serializers.ClientCartUpdateSerializer
    queryset = client_models.ClientCart.objects.all()