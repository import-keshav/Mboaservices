from django import forms

from rest_framework import serializers

from . import models

from User import models as user_models
from User import serializers as user_serializer


class ClientPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Client
        fields = '__all__'
    def validate(self, data):
        if not 'user' in data:
            raise forms.ValidationError('Include User ID in data')
        if models.Client.objects.filter(user=data['user']).first():
            raise forms.ValidationError('Client Already exists with this credentials')
        return data


class ClientGetSerializer(serializers.ModelSerializer):
    user = user_serializer.UserSerializer()
    class Meta:
        model = models.Client
        fields = '__all__'


class ClientNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ClientNotification
        fields = '__all__'
    def validate(self, data):
        if not 'client' in data:
            raise forms.ValidationError('Include Client in data')
        return data
