from django import forms

from rest_framework import serializers

from . import models

from User import models as user_models
from User import serializers as user_serializer
from Reviews import models as review_models
from Orders import models as order_models

class RestaurantPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Restaurant
        fields = '__all__'


class RestaurantUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Restaurant
        fields = '__all__'


class RestaurantGetSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    num_of_incoming_orders = serializers.SerializerMethodField()
    num_of_outgoing_orders = serializers.SerializerMethodField()


    def get_category(self, obj):
        return [{"name":cat.name, "id": cat.pk} for cat in obj.category.all()]
    def get_num_of_incoming_orders(self, obj):
        return len(order_models.IncomingOrder.objects.filter(restaurant=obj))
    def get_num_of_outgoing_orders(self, obj):
        return len(order_models.OngoingOrder.objects.filter(restaurant=obj))

    class Meta:
        model = models.Restaurant
        fields = ['name', 'latitude', 'longitude', 'rating', 'mobile',
            'is_open', 'address', 'category', 'image', 'num_of_incoming_orders',
            'num_of_outgoing_orders', 'id']


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


class RestaurantPromocodeUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RestaurantPromocode
        fields = '__all__'


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
    category = serializers.SerializerMethodField()

    def get_category(self, obj):
        return [{"name":cat.name, "id": cat.pk} for cat in obj.category.all()]

    class Meta:
        model = models.RestaurantPromocode
        fields = '__all__'


class GlobalPromocodeGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.GlobalPromocode
        fields = '__all__'
