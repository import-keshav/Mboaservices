from django import forms

from rest_framework import serializers

from . import models as invigilator_models
from . import serializers as invigilator_serializer
from Client import serializers as client_serializer

class InvigilatorGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = invigilator_models.Invigilator
        fields = '__all__'


class InvigilatorClientMessageGetSerializer(serializers.ModelSerializer):
    invigilator = InvigilatorGetSerializer()
    client = client_serializer.ClientGetSerializer()
    class Meta:
        model = invigilator_models.InvigilatorClientMessage
        fields = '__all__'