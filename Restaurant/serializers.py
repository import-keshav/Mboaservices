from django import forms

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from . import models

from User import models as user_models
from User import serializers as user_serializer


class RestaurantPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Restaurant
        fields = '__all__'
    def validate(self, data):
        if not 'owner' in data:
            raise forms.ValidationError('Include owner id in data')
        return data



class RestaurantGetSerializer(serializers.ModelSerializer):
    owner = user_serializer.UserSerializer()
    class Meta:
        model = models.Restaurant
        fields = '__all__'


class RestaurantEmployeePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RestaurantEmployee
        fields = '__all__'

    def validate(self, data):
        if not 'restaurant' in data:
            raise forms.ValidationError('Include restaurant id in data')
        if not 'user' in data:
            raise forms.ValidationError('Include user id in data')
        user = user_models.User.objects.filter(pk=data['user'].pk).first()
        restaurant =  models.Restaurant.objects.filter(pk=data['restaurant'].pk).first()
        if models.RestaurantEmployee.objects.filter(user=user, restaurant=restaurant):
            raise forms.ValidationError('User already a employee in the restaurant')
        return data


class RestaurantEmployeeGetSerializer(serializers.ModelSerializer):
    user = user_serializer.UserSerializer()
    restaurant = RestaurantGetSerializer()
    class Meta:
        model = models.RestaurantEmployee
        fields = '__all__'


class RestaurantImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RestaurantImage
        fields = '__all__'

    def validate(self, data):
        if not 'restaurant' in data:
            raise forms.ValidationError('Include restaurant id in data')
        if not 'image' in data:
            raise forms.ValidationError('Include image in data')
        return data


class RestaurantPromocodePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RestaurantPromocode
        fields = '__all__'

    def validate(self, data):
        if not 'promocode' in data:
            raise forms.ValidationError('Include Promocode in Data')
        if not 'restaurant' in data:
            raise forms.ValidationError('Include Restaurant ID In Data')
        return data


class RestaurantPromocodeGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RestaurantPromocode
        fields = '__all__'


class RestaurantDriverPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RestaurantDriver
        fields = '__all__'

    def validate(self, data):
        if not 'name' in data:
            raise forms.ValidationError('Include Name in Driver Data')
        if not 'restaurant' in data:
            raise forms.ValidationError('Include Restaurant ID In Data')
        return data


class RestaurantDriverGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RestaurantDriver
        fields = '__all__'