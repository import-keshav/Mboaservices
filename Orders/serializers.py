from django import forms

from rest_framework import serializers

from . import models
from Client import serializers as client_serializer
from Invigilator import models as invigilator_models
from Invigilator import serializers as invigilator_serializer
from Dishes import models as dish_models
from Dishes import serializers as dish_serializer
from Restaurant import serializers as restaurant_serializer


class GetOrderOnlySerializer(serializers.ModelSerializer):
    dishes = serializers.SerializerMethodField()
    restaurant = restaurant_serializer.RestaurantGetSerializer()

    def get_dishes(self, obj):
        return [GetOrderDishSerializer(dish).data for dish in models.OrderDish.objects.filter(order=obj)]
    class Meta:
        model = models.Order
        fields = '__all__'


class GetOrderSerializer(serializers.ModelSerializer):
    client = client_serializer.ClientGetSerializer()
    dishes = serializers.SerializerMethodField()
    restaurant = restaurant_serializer.RestaurantGetSerializer()
    invigilator = serializers.SerializerMethodField()

    def get_dishes(self, obj):
        return [GetOrderDishSerializer(dish).data for dish in models.OrderDish.objects.filter(order=obj)]

    def get_invigilator(self, obj):
        invigilator = invigilator_models.InvigilatorRestaurant.objects.filter(restaurant=obj.restaurant).first()
        if invigilator:
            return invigilator_serializer.InvigilatorGetSerializer(invigilator.invigilator).data
        return {}

    class Meta:
        model = models.Order
        fields = '__all__'


class CreateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Order
        fields = '__all__'
    def validate(self, data):
        valid_keys = ['restaurant', 'client', 'payment_method', 'total_amount']
        if not data:
            raise forms.ValidationError('Include ' + ' ,'.join(valid_keys) + ' in data')
        for key in valid_keys:
            if key not in data:
                raise forms.ValidationError('Include ' + key + ' in data')
        return data


class CreateOrderDisheSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.OrderDish
        fields = '__all__'
    def validate(self, data):
        valid_keys = ['order', 'dish', 'quantity', 'add_ons']
        if not data:
            raise forms.ValidationError('Include ' + ' ,'.join(valid_keys) + ' in data')
        for key in data:
            if key not in valid_keys:
                raise forms.ValidationError('Include ' + key + ' in data')
        return data


class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Order
        fields = '__all__'


class GetOrderDishSerializer(serializers.ModelSerializer):
    dish = dish_serializer.DishGetSerializer()
    add_ons = serializers.SerializerMethodField()

    def get_add_ons(self, obj):
        return [dish_serializer.DishAddOnsGetSerializer(add_on).data for add_on in obj.add_ons.all()]
    class Meta:
        model = models.OrderDish
        fields = '__all__'


class GetClientRestaurantPastOrdersSerializer(serializers.ModelSerializer):
    client = client_serializer.ClientGetSerializer()
    dishes = serializers.SerializerMethodField()
    restaurant = restaurant_serializer.RestaurantGetSerializer()
    invigilator = serializers.SerializerMethodField()

    def get_dishes(self, obj):
        return [GetOrderDishSerializer(dish).data for dish in models.OrderDish.objects.filter(order=obj)]

    def get_invigilator(self, obj):
        invigilator = invigilator_models.InvigilatorRestaurant.objects.filter(restaurant=obj.restaurant).first()
        if invigilator:
            return invigilator_serializer.InvigilatorGetSerializer(invigilator.invigilator).data
        return {}
    class Meta:
        model = models.Order
        fields = '__all__'
