from django import forms

from rest_framework import serializers

from . import models

from User import models as user_models
from User import serializers as user_serializer
from Dishes import serializers as dish_serializer

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


class ClientUpdateSerializer(serializers.ModelSerializer):
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


class ClientCartPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ClientCart
        fields = '__all__'
    def validate(self, data):
        if not 'client' in data:
            raise forms.ValidationError('Include Client in data')
        if not 'restaurant' in data:
            raise forms.ValidationError('Include Restaurant in data')
        if not 'dish' in data:
            raise forms.ValidationError('Include Dish in data')
        return data


class ClientCartGetSerializer(serializers.ModelSerializer):
    dish = dish_serializer.DishSerializer()
    class Meta:
        model = models.ClientCart
        fields = '__all__'


class ClientCartUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ClientCart
        fields = '__all__'
