from django import forms

from rest_framework import serializers

from . import models
from Client import models as client_models
from Restaurant import models as restaurant_models
from Restaurant import serializers as restaurant_serializers


class GetClientReviewSerializer(serializers.ModelSerializer):
    restaurant = restaurant_serializers.RestaurantGetSerializer()
    class Meta:
        model = models.ClientReview
        fields = '__all__'


class PostClientReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ClientReview
        fields = '__all__'
    def validate(self, data):
        valid_keys = ['client', 'restaurant', 'points', 'comment']
        for key in valid_keys:
            if not key in data:
                raise forms.ValidationError(key + " is missing")
        if models.ClientReview.objects.filter(client=data['client'], restaurant=data['restaurant']).first():
            raise forms.ValidationError("Review Already Done")
        self.update_restaurant_rating_info(data)
        return data

    def update_restaurant_rating_info(self, data):
        if not models.RestaurantReviewsInfo.objects.filter(restaurant=data['restaurant']):
            restaurant_review = models.RestaurantReviewsInfo(
                restaurant=data['restaurant'], number_of_reviews=0, points=0)
            restaurant_review.save()
        restaurant_review = models.RestaurantReviewsInfo.objects.filter(restaurant=data['restaurant']).first()
        restaurant_review.number_of_reviews +=1
        restaurant_review.points += data['points']
        restaurant = restaurant_models.Restaurant.objects.filter(pk=data['restaurant'].pk).first()
        restaurant.rating = restaurant_review.points//restaurant_review.number_of_reviews
        restaurant.save()
        restaurant_review.save()
