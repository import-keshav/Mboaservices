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
