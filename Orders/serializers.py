from django import forms

from rest_framework import serializers

from . import models


class CreateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Order
        fields = '__all__'
    def validate(self, data):
        valid_keys = ['restaurant', 'client', 'payment_method', 'total_amount']
        if not data:
            raise forms.ValidationError('Include ' + ' ,'.join(valid_keys) + ' in data')
        for key in data:
            if key not in valid_keys:
                raise forms.ValidationError('Include ' + key + ' in data')
        return data


class CreateOrderDisheSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.OrderDish
        fields = '__all__'
    def validate(self, data):
        valid_keys = ['order', 'dish', 'quantity']
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
    class Meta:
        model = models.OrderDish
        fields = '__all__'


class GetClientRestaurantPastOrdersSerializer(serializers.ModelSerializer):
    dishes = serializers.SerializerMethodField()
    def get_dishes(self, obj):
        return [GetOrderDishSerializer(dish).data for dish in models.OrderDish.objects.filter(order=obj)]

    class Meta:
        model = models.Order
        fields = '__all__'
