from django import forms

from rest_framework import serializers

from . import models

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

class DishGetSerializer(serializers.ModelSerializer):
    categories = serializers.SerializerMethodField()

    def get_categories(self, obj):
        return [{"name":cat.name, "id": cat.pk} for cat in obj.categories.all()]
    class Meta:
        model = models.Dish
        fields = '__all__'


class DishUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Dish
        fields = '__all__'


class DishImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DishImage
        fields = '__all__'
    def validate(self, data):
        if not 'dish' in data:
            raise forms.ValidationError('Include dish of image')
        if not 'image' in data:
            raise forms.ValidationError('Include image')
        return data
