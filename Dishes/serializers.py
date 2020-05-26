from django import forms

from rest_framework import serializers

from . import models

from Restaurant import serializers as restaurant_serializers

class DishPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Dish
        fields = '__all__'
    def validate(self, data):
        if not 'name' in data:
            raise forms.ValidationError('Include name of dish')
        if not 'restaurant' in data:
            raise forms.ValidationError('Include restaurant of dish')
        if not 'price' in data:
            raise forms.ValidationError('Include price of dish')
        return data


class DishAddOnsGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DishAddOns
        fields = '__all__'


class DishAddOnsPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DishAddOns
        fields = '__all__'
    def validate(self, data):
        if not 'name' in data:
            raise forms.ValidationError('Include name of dish addon')
        if not 'dish' in data:
            raise forms.ValidationError('Include dish of dish add on')
        if not 'price' in data:
            raise forms.ValidationError('Include price of dish add on')
        return data


class DishGetSerializer(serializers.ModelSerializer):
    categories = serializers.SerializerMethodField()
    add_ons = serializers.SerializerMethodField()

    def get_categories(self, obj):
        return [{"name":cat.name, "id": cat.pk} for cat in obj.categories.all()]

    def get_add_ons(self, obj):
        return [DishAddOnsGetSerializer(addon).data for addon in models.DishAddOns.objects.filter(dish=obj)]

    class Meta:
        model = models.Dish
        fields = '__all__'


class DishUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Dish
        fields = '__all__'


class DishSearchFilterSerializer(serializers.ModelSerializer):
    categories = serializers.SerializerMethodField()
    restaurant = restaurant_serializers.RestaurantGetSerializer()

    def get_categories(self, obj):
        return [{"name":cat.name, "id": cat.pk} for cat in obj.categories.all()]

    class Meta:
        model = models.Dish
        fields = '__all__'
