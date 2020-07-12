from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from rest_framework import generics, status, filters

from . import models as invigilator_models
from . import serializers as invigilator_serializer
from Client import models as client_models


class GetInvigilatorClientChat(generics.ListAPIView):
    renderer_classes = [JSONRenderer]
    serializer_class = invigilator_serializer.InvigilatorClientMessageGetSerializer

    def get_queryset(self):
        invigilator = invigilator_models.Invigilator.objects.filter(pk=self.kwargs['invigilator']).first()
        client = client_models.Client.objects.filter(pk=self.kwargs['client']).first()
        return invigilator_models.InvigilatorClientMessage.objects.filter(client=client, invigilator=invigilator)

