from django import forms

from rest_framework import serializers

from . import models

from User import models as user_models
from User import serializers as user_serializer
from Dishes import serializers as dish_serializer
from Dishes import models as dish_models
from Restaurant import serializers as restaurant_serializer

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
        if not 'add_ons' in data:
            raise forms.ValidationError('Include add_ons in data')
        self.validate_client_cart_data(data)
        return data

    def validate_client_cart_data(self, data):
        if data['dish'].restaurant != data['restaurant']:
            raise forms.ValidationError("Invalid Dish ID, Dish doesn't match with Restaurant")
        valid_dish_add_ons = dish_models.DishAddOns.objects.filter(dish=data['dish'])
        # print(valid_dish_add_ons)
        for add_on in data['add_ons']:
            if add_on not in valid_dish_add_ons:
                raise forms.ValidationError("Invalid Dish Add Ons ID, Dish Add Ons doesn't match with Dish")


class ClientCartGetSerializer(serializers.ModelSerializer):
    dish = dish_serializer.DishGetSerializer()
    add_ons = serializers.SerializerMethodField()
    restaurant = restaurant_serializer.RestaurantGetSerializer()
    def get_add_ons(self, obj):
        return[dish_serializer.DishAddOnsGetSerializer(add_on).data for add_on in obj.add_ons.all()]
    class Meta:
        model = models.ClientCart
        fields = '__all__'


class ClientCartUpdateSerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, obj):
        cart_items =  models.ClientCart.objects.filter(client=obj.client)
        total_price = 0
        for cart_item in cart_items:
            price = cart_item.dish.price * cart_item.num_of_items
            for add_on in cart_item.add_ons.all():
                if not add_on.is_free:
                    price += (add_on.price * cart_item.num_of_items)
            total_price +=price
        return total_price
    class Meta:
        model = models.ClientCart
        fields = '__all__'
